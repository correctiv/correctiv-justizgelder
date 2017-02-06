# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correctiv_justizgelder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='search_index',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
    ]
