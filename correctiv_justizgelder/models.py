# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Count, Max
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField


GERMAN_STATES = (
    ('baden-wuerttemberg', _(u'Baden-Württemberg')),
    ('bayern', _(u'Bavaria')),
    ('berlin', _(u'Berlin')),
    ('brandenburg', _(u'Brandenburg')),
    ('bremen', _(u'Bremen')),
    ('hamburg', _(u'Hamburg')),
    ('hessen', _(u'Hesse')),
    ('mecklenburg-vorpommern', _(u'Mecklenburg-Western Pomerania')),
    ('niedersachsen', _(u'Lower Saxony')),
    ('nordrhein-westfalen', _(u'North Rhine-Westphalia')),
    ('rheinland-pfalz', _(u'Rhineland-Palatinate')),
    ('saarland', _(u'Saarland')),
    ('sachsen', _(u'Saxony')),
    ('sachsen-anhalt', _(u'Saxony-Anhalt')),
    ('schleswig-holstein', _(u'Schleswig-Holstein')),
    ('thueringen', _(u'Thuringia'))
)
GERMAN_STATES_DICT = dict(GERMAN_STATES)


class OrganisationManager(models.Manager):
    def search(self, query=None, **kwargs):

        filters = {}
        fine_filter = {}
        if query:
            query = query.strip().encode('utf-8').split()
            fine_filter['search_index__ft_startswith'] = query
            filters['fines__search_index__ft_startswith'] = query

        ordering = '-filtered_amount'

        for key, val in kwargs.items():
            if val is not None and val != '':
                filters['fines__%s' % key] = val

        q = (
            Organisation.objects.all()
            .filter(**filters)
            .annotate(
                filtered_amount=Sum('fines__amount'),
                fine_count=Count('fines')
            )
            .order_by(ordering)
        )

        fines = Fine.objects.filter(**fine_filter)

        aggs = {
            'total_sum': q.aggregate(
                total_sum=Sum('filtered_amount'))['total_sum'] or 0.0,
            'max_amount': q.aggregate(
                max_amount=Max('filtered_amount'))['max_amount'] or 0.0,
            'years': fines.values('year').annotate(
                doc_count=Count('year')).order_by(),
            'states': fines.values('state').annotate(
                doc_count=Count('state')).order_by(),
            'doc_count': fines.count()
        }
        return q, aggs


class Organisation(models.Model):
    name = models.CharField(max_length=512, db_index=True)
    slug = models.SlugField(max_length=255)
    sum_fines = models.DecimalField(null=True, decimal_places=2, max_digits=19)
    note = models.TextField(blank=True)
    treasury = models.BooleanField(default=False)

    objects = OrganisationManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('justizgelder:organisation_detail',
                       kwargs={'slug': self.slug})


class FineManager(SearchManager):
    def all_with_amount(self):
        return self.get_queryset().exclude(amount=0.0)


class Fine(models.Model):

    DEPARTMENTS = (
        ('sta', _(u'Prosecutor')),
        ('justiz', _(u'Ministry of Justice')),
        ('lg', _(u'State Court')),
        ('ag', _(u'Local Court')),
        ('olg', _(u'Upper State Court')),
    )
    DEPARTMENTS_DICT = dict(DEPARTMENTS)

    organisation = models.ForeignKey(Organisation, related_name='fines')
    name = models.CharField(max_length=512)
    original_name = models.CharField(max_length=512)

    year = models.SmallIntegerField(db_index=True)

    state = models.CharField(max_length=25, choices=GERMAN_STATES, db_index=True)
    department = models.CharField(max_length=10, choices=DEPARTMENTS)
    department_detail = models.CharField(max_length=255, blank=True)

    amount = models.DecimalField(decimal_places=2, max_digits=19)
    amount_received = models.DecimalField(null=True, decimal_places=2,
                                          max_digits=19, blank=True)

    address = models.TextField(blank=True)
    file_reference = models.CharField(max_length=255, blank=True)
    source_file = models.CharField(max_length=255, blank=True)
    bank_details = models.TextField(blank=True)
    org_details = models.TextField(blank=True)
    filename = models.CharField(max_length=255)
    reference_id = models.CharField(max_length=255)

    note = models.TextField(blank=True)

    city = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=10, blank=True)

    treasury = models.BooleanField(default=False, db_index=True)

    search_index = VectorField()

    objects = FineManager(
        fields=[
            ('name', 'A'),
            ('city', 'B'),
            ('postcode', 'C'),
            ('address', 'D'),
            ('department_detail', 'D'),
        ],
        config='pg_catalog.german',
        search_field='search_index',
        auto_update_search_field=True
    )

    objects = FineManager()

    class Meta:
        ordering = ('-year', 'state', '-amount')

    def __unicode__(self):
        return self.reference_id

    @property
    def state_label(self):
        return GERMAN_STATES_DICT[self.state]

    @property
    def department_label(self):
        return self.DEPARTMENTS_DICT[self.department] + ' ' + self.department_detail

    @property
    def source_file_extension(self):
        if self.source_file and '.' in self.source_file:
            return self.source_file.rsplit('.', 1)[1]
        return '???'

    @property
    def source_file_url(self):
        if self.source_file:
            if not self.source_file.rsplit('.', 1)[0].endswith('_'):
                # File is not 'secret'
                return 'investigations/justizgelder/' + self.source_file
        return ''
