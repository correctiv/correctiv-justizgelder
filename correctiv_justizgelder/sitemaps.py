from django.contrib.sitemaps import Sitemap

from .models import Organisation


def update_sitemap(sitemap_dict):
    sitemap_dict.update({
        'justizgelder-organisations': OrganisationSitemap
    })
    return sitemap_dict


class OrganisationSitemap(Sitemap):
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        """
        Return published entries.
        """
        return Organisation.objects.all()
