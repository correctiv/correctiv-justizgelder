# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correctiv_justizgelder', '0004_auto_20150429_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='reference_id',
            field=models.CharField(max_length=255, db_index=True),
            preserve_default=True,
        ),
    ]
