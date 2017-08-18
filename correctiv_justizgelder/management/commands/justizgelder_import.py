import decimal

import unicodecsv
from tqdm import tqdm
from slugify import slugify

from django.core.management.base import BaseCommand
from django.utils import translation
from django.conf import settings

from ...models import Fine, Organisation

BULK_SIZE = 1000


class Command(BaseCommand):
    help = "Import CSV"

    def add_arguments(self, parser):
        parser.add_argument('filename', help='filename')

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)

        filename = options['filename']

        self.staatskasse, created = Organisation.objects.get_or_create(
            name='Staatskasse', slug='staatskasse',
            treasury=True
        )

        collection = []
        bulk_insert_count = 0
        for fine in self.get_fine_objects(filename):
            collection.append(fine)
            if len(collection) > BULK_SIZE:
                bulk_insert_count += 1
                self.stdout.write('Bulk insert %d\n' % bulk_insert_count)
                Fine.objects.bulk_create(collection)
                collection = []

        Fine.objects.bulk_create(collection)
        self.stdout.write('Creating aggregates...\n')
        self.create_aggregates()

    def get_fine_objects(self, filename):
        for row in tqdm(unicodecsv.DictReader(open(filename))):
            fine = None
            try:
                fine = Fine.objects.get(
                    reference_id=row['id']
                )
            except Fine.DoesNotExist:
                yield self.create_from_row(row, fine=fine)

    def create_from_row(self, row, fine=None):
        if fine is None:
            fine = Fine()

        org_slug = slugify(row['name'])
        old_org_slug = slugify(row['name'])

        if org_slug != old_org_slug:
            Organisation.objects.filter(slug=old_org_slug).delete()

        treasury = False

        if bool(int(row.get('staatskasse', '0'))):
            org = self.staatskasse
            treasury = True
        else:
            try:
                org = Organisation.objects.get(slug=org_slug)
            except Organisation.DoesNotExist:
                org = Organisation.objects.create(name=row['name'], slug=org_slug)

        fine.treasury = treasury
        fine.organisation = org
        fine.name = row['name']
        fine.original_name = row['orig_name']
        # path of the form data/badenwuerttemberg/2013/justiz/justiz_bawue_2013.csv
        parts = row['path'].split('/')
        fine.state = parts[1]
        fine.year = int(parts[2])
        if parts[3] not in Fine.DEPARTMENTS_DICT:
            fine.department = ''
        else:
            fine.department = parts[3]
        department_detail = parts[4].split('_')
        if len(department_detail) > 3:
            department_detail = department_detail[3].title()
            if department_detail != str(fine.year):
                fine.department_detail = department_detail

        fine.amount = decimal.Decimal(row['betrag'])
        if row.get('betrag_eingegangen'):
            fine.amount_received = decimal.Decimal(row['betrag_eingegangen'])

        fine.address = row['adresse']
        fine.file_reference = row['aktenzeichen']
        fine.filename = row['path']
        # fine.note = row['anmerkungen']
        fine.source_file = row['source']
        fine.reference_id = row['id']
        fine.city = row['ort']
        fine.postcode = row['plz']

        fine.bank_details = u'\n'.join(
            row.get(k) for k in (
                'blz',
                'kto',
                'kreditinstitut',
                'bank',
            ) if row.get(k))

        fine.org_details = row.get('anmerkungen', '')

        return fine

    def create_aggregates(self):
        from django.db import connections

        if 'data' in connections:
            con = connections['data']
        else:
            con = connections['default']

        cursor = con.cursor()
        cursor.execute("""UPDATE correctiv_justizgelder_organisation
            SET sum_fines=(
                SELECT COALESCE(SUM(correctiv_justizgelder_fine.amount), 0) FROM
                 correctiv_justizgelder_fine WHERE
                  correctiv_justizgelder_fine.organisation_id=correctiv_justizgelder_organisation.id
        );""")
