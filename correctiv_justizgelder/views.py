from django.views.generic import ListView, DetailView

from .forms import OrganisationSearchForm
from .models import Organisation


class OrganisationSearchView(ListView):
    template_name = 'justizgelder/search.html'
    paginate_by = 25

    def get_queryset(self):
        self.form = OrganisationSearchForm(self.request.GET)
        result, self.aggregates = self.form.search()
        return result

    def get_context_data(self, **kwargs):
        context = super(OrganisationSearchView,
                        self).get_context_data(**kwargs)
        context['aggregates'] = self.aggregates
        context['query'] = self.request.GET.get('q')
        context['form'] = self.form
        context['base_template'] = 'justizgelder/search_base.html'
        if self.request.GET.get('embed'):
            context['base_template'] = 'justizgelder/embed_base.html'
        return context


class OrganisationDetail(DetailView):
    template_name = 'justizgelder/organisation_detail.html'
    model = Organisation

    def get_context_data(self, **kwargs):
        context = super(OrganisationDetail, self).get_context_data(**kwargs)
        return context
