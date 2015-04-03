from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import OrganisationSearchView, OrganisationDetail


urlpatterns = patterns('',
    url(r'^$',
        OrganisationSearchView.as_view(),
        name='search'),
    url(_(r'^recipient/(?P<slug>[\w-]+)/$'),
        OrganisationDetail.as_view(),
        name='organisation_detail'),
)
