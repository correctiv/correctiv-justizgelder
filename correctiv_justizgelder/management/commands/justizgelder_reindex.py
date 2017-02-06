from django.core.management.base import BaseCommand
from django.utils import translation
from django.conf import settings

from ...models import Fine


class Command(BaseCommand):
    help = "Reindex search vector"

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)

        Fine.objects.update_search_index()
