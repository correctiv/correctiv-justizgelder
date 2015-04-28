from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Organisation, GERMAN_STATES


class OrganisationSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label=_('Search'),
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'class': 'form-control',
                'placeholder': _('Your search')
            }))

    amount_gte = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput)

    amount_lte = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput)

    state = forms.ChoiceField(
        choices=GERMAN_STATES,
        required=False,
        widget=forms.HiddenInput)

    treasury = forms.TypedChoiceField(
        label=_('Include treasury'),
        choices=[
            ('', 'Include treasury'),
            ('0', _('Exclude treasury')),
            ('1', _('Only treasury')),
        ],
        empty_value=None,
        required=False,
        coerce=lambda x: bool(int(x))
    )

    year = forms.TypedChoiceField(
        choices=(
            (2007, '2007'),
            (2008, '2008'),
            (2009, '2009'),
            (2010, '2010'),
            (2011, '2011'),
            (2012, '2012'),
            (2013, '2013'),
            (2014, '2014')
        ),
        required=False,
        coerce=int,
        empty_value='',
        widget=forms.HiddenInput)

    sort = forms.ChoiceField(
        choices=(
            ('amount:desc', _('Amount')),
            ('name:asc', _('Name')),
        ),
        initial='amount:desc',
        required=False,
        widget=forms.RadioSelect)

    FILTERS = {
        'state': 'state',
        'year': 'year'
    }
    RANGES = (
        'amount_lte',
        'amount_gte'
    )

    def __init__(self, data, **kwargs):
        data = data.copy()
        data.setdefault('sort', 'amount:desc')
        super(OrganisationSearchForm, self).__init__(data=data, **kwargs)

    def _search(self, query):
        return Organisation.objects.search(
            query=self.cleaned_data.get('q'),
            sort=self.cleaned_data.get('sort'),
            state=self.cleaned_data.get('state'),
            year=self.cleaned_data.get('year'),
            treasury=self.cleaned_data.get('treasury'),
            amount__gte=self.cleaned_data.get('amount__gte'),
            amount__lte=self.cleaned_data.get('amount__lte')
        )

    def get_filters(self):
        filters = {}
        for key in self.FILTERS:
            filters[self.FILTERS[key]] = self.cleaned_data[key]
        return filters

    def get_ranges(self):
        return {key: self.cleaned_data[key] for key in self.RANGES}

    def search(self):
        if not self.is_valid():
            import ipdb; ipdb.set_trace()

            return Organisation.objects.all(), {}

        sqs = self._search(self.cleaned_data['q'])

        return sqs
