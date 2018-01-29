# -*- encoding: utf-8 -*-
from django.core.management import BaseCommand

from ...models import Fine


class Command(BaseCommand):
    help = "Rewrites the paths to the source files that are visible on the website to" \
           "not contain umlauts anymore. Make sure to update the files themselves too!"

    def handle(self, *args, **options):
        for letter in [u"a\u0308", u"o\u0308", u"u\u0308"]:
            matching_fines = Fine.objects.filter(source_file__contains=letter)
            source_files = {fine["source_file"] for fine in matching_fines.values("source_file")}
            for filename in source_files:
                new_name = filename.replace(u"\u0308", "e")
                print("Renaming '{}' to '{}'".format(filename, new_name))
                Fine.objects.filter(source_file=filename).update(source_file=new_name)
        print("All Done. Do not forget to also update the files on the hard drive")
