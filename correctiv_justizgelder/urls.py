from functools import wraps

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page

from .views import OrganisationSearchView, OrganisationDetail

CACHE_TIME = 15 * 60


def c(view):
    @wraps(view)
    def cache_page_anonymous(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view(request, *args, **kwargs)
        return cache_page(CACHE_TIME)(view)(request, *args, **kwargs)
    return cache_page_anonymous


urlpatterns = patterns('',
    url(r'^$', c(OrganisationSearchView.as_view()), name='search'),
    url(_(r'^recipient/(?P<slug>[^/]+)/$'),
        c(OrganisationDetail.as_view()),
        name='organisation_detail'),
)
