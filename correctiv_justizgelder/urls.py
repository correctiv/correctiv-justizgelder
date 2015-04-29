from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page

from .views import OrganisationSearchView, OrganisationDetail

CACHE_TIME = 15 * 60


def c(view):
    return cache_page(CACHE_TIME)(view)


urlpatterns = patterns('',
    url(r'^$', c(OrganisationSearchView.as_view()), name='search'),
    url(_(r'^recipient/(?P<slug>[\w-]+)/$'),
        c(OrganisationDetail.as_view()),
        name='organisation_detail'),
)
