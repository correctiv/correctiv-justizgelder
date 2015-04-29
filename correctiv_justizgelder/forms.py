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

    treasury = forms.TypedChoiceField(
        label=_('Include treasury'),
        choices=[
            ('0', _('Exclude treasury')),
            ('-', _('Include treasury')),
            ('1', _('Only treasury')),
        ],
        initial=False,
        empty_value=None,
        required=False,
        coerce=lambda x: None if x == '-' else bool(int(x))
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
            return Organisation.objects.all(), {}

        sqs = self._search(self.cleaned_data['q'])

        return sqs
