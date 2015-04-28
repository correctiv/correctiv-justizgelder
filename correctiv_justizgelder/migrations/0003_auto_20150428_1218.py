# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correctiv_justizgelder', '0002_fine_search_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='treasury',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organisation',
            name='treasury',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
