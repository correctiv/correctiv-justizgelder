# -*- encoding: utf-8 -*-
from django.core.management import BaseCommand
import requests

from ...models import Fine


class Command(BaseCommand):
    help = "Check all published files for their existence on the server"

    def handle(self, *args, **options):
        for fine in Fine.objects.distinct("source_file").order_by("source_file").values("source_file").all():
            url = "https://correctiv.org/media/investigations/justizgelder/{}"
            response = requests.head(url.format(fine["source_file"]))
            if response.status_code != 200:
                print("Not found: {}".format(fine["source_file"]))
