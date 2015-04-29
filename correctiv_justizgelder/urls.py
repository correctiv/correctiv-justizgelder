from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import decorator_from_middleware_with_args
from django.middleware.cache import CacheMiddleware

from .views import OrganisationSearchView, OrganisationDetail

CACHE_TIME = 15 * 60


def cache_page_anonymous(*args, **kwargs):
    """
    Decorator to cache Django views only for anonymous users.
    Use just like the decorator cache_page:

    @cache_page_anonymous(60 * 30)  # cache for 30 mins
    def your_view_here(request):
        ...
    """
    key_prefix = kwargs.pop('key_prefix', None)
    return decorator_from_middleware_with_args(CacheMiddleware)(
        cache_timeout=args[0],
        key_prefix=key_prefix,
        cache_anonymous_only=True)


def c(view):
    return cache_page_anonymous(CACHE_TIME)(view)


urlpatterns = patterns('',
    url(r'^$', c(OrganisationSearchView.as_view()), name='search'),
    url(_(r'^recipient/(?P<slug>[\w-]+)/$'),
        c(OrganisationDetail.as_view()),
        name='organisation_detail'),
)
