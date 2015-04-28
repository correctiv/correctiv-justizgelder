# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('correctiv_justizgelder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='search_index',
            field=djorm_pgfulltext.fields.VectorField(),
            preserve_default=True,
        ),
    ]
