"""Application hooks for blog"""
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class JustizgelderApphook(CMSApp):
    name = _('Court Donations Database')
    app_name = 'justizgelder'
    urls = ['correctiv_justizgelder.urls']


apphook_pool.register(JustizgelderApphook)
