# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Count, Max
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.search import (SearchVectorField, SearchVector,
        SearchVectorExact, SearchQuery)

SEARCH_LANG = 'german'


class SearchVectorStartsWith(SearchVectorExact):
    """This lookup scans for full text index entries that BEGIN with
    a given phrase, like:
    will get translated to
        ts_query('Foobar:* & Baz:* & Quux:*')
    """
    lookup_name = 'startswith'

    def process_rhs(self, qn, connection):
        if not hasattr(self.rhs, 'resolve_expression'):
            config = getattr(self.lhs, 'config', None)
            self.rhs = SearchQuery(self.rhs, config=config)
        rhs, rhs_params = super(SearchVectorExact, self).process_rhs(qn, connection)
        rhs = '(to_tsquery(%s::regconfig, %s))'
        parts = (s.replace("'", '') for s in rhs_params[1].split())
        rhs_params[1] = ' & '.join("'%s':*" % s for s in parts if s)
        return rhs, rhs_params

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s @@ %s' % (lhs, rhs), params


SearchVectorField.register_lookup(SearchVectorStartsWith)


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
            query = SearchQuery(query.strip(), config=SEARCH_LANG)
            fine_filter['search_vector__startswith'] = query
            filters['fines__search_vector__startswith'] = query

        amount_lte = kwargs.pop('amount__lte', None)
        amount_gte = kwargs.pop('amount__gte', None)

        for key, val in kwargs.items():
            if val is not None and val != '':
                filters['fines__%s' % key] = val

        q = Organisation.objects.filter(**filters)

        if filters or amount_lte is not None or amount_gte is not None:
            amount_col = 'filtered_amount'
            q = q.annotate(
                filtered_amount=Sum('fines__amount'),
                fine_count=Count('fines')
            )
            a_filters = {}

            if amount_lte is not None:
                a_filters['filtered_amount__lte'] = amount_lte
            if amount_gte is not None:
                a_filters['filtered_amount__gte'] = amount_gte

            final_q = q
            if a_filters:
                final_q = final_q.filter(**a_filters)

        else:
            amount_col = 'sum_fines'
            final_q = q.annotate(
                fine_count=Count('fines')
            )

        ordering = '-%s' % amount_col
        ordered_final_q = final_q.order_by(ordering)

        fines = Fine.objects.filter(**fine_filter).order_by()

        aggs = {
            'total_sum': final_q.aggregate(
                total_sum=Sum(amount_col))['total_sum'] or 0.0,
            'max_amount': q.aggregate(
                max_amount=Max(amount_col))['max_amount'] or 0.0,
            'years': fines.values('year').annotate(
                doc_count=Count('year')),
            'states': fines.values('state').annotate(
                doc_count=Count('state')),
            'doc_count': fines.count()
        }
        return ordered_final_q, aggs


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

    @property
    def amount(self):
        return getattr(self, 'filtered_amount', self.sum_fines)


class FineManager(models.Manager):
    def update_search_index(self):
        search_vector = (
            SearchVector('name', weight='A', config=SEARCH_LANG) +
            SearchVector('city', weight='B', config=SEARCH_LANG) +
            SearchVector('postcode', weight='C', config=SEARCH_LANG) +
            SearchVector('address', weight='D', config=SEARCH_LANG) +
            SearchVector('department_detail', weight='D',
                         config=SEARCH_LANG)
        )
        Fine.objects.update(search_vector=search_vector)

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
    reference_id = models.CharField(max_length=255, db_index=True)

    note = models.TextField(blank=True)

    city = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=10, blank=True)

    treasury = models.BooleanField(default=False, db_index=True)

    search_vector = SearchVectorField(null=True)

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
        if self.department_detail:
            return u'%s %s' % (self.DEPARTMENTS_DICT[self.department], self.department_detail)
        else:
            return self.DEPARTMENTS_DICT[self.department]

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
