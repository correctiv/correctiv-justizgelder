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
                'placeholder': _('e.g. Polizeisport')
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

    MIN_YEAR, MAX_YEAR = 2007, 2016
    year = forms.TypedChoiceField(
        choices=[
            (year, str(year)) for year in range(MIN_YEAR, MAX_YEAR + 1)
        ],
        required=False,
        coerce=int,
        empty_value='',
        widget=forms.HiddenInput)

    def __init__(self, data, **kwargs):
        data = data.copy()
        super(OrganisationSearchForm, self).__init__(data=data, **kwargs)

    def _search(self, query):
        return Organisation.objects.search(
            query=self.cleaned_data.get('q'),
            state=self.cleaned_data.get('state'),
            year=self.cleaned_data.get('year'),
            treasury=self.cleaned_data.get('treasury'),
            amount__gte=self.cleaned_data.get('amount_gte'),
            amount__lte=self.cleaned_data.get('amount_lte')
        )

    def search(self):
        if not self.is_valid():
            return Organisation.objects.search()

        sqs = self._search(self.cleaned_data['q'])

        return sqs
