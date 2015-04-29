# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correctiv_justizgelder', '0003_auto_20150428_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='state',
            field=models.CharField(db_index=True, max_length=25, choices=[(b'baden-wuerttemberg', 'Baden-W\xfcrttemberg'), (b'bayern', 'Bavaria'), (b'berlin', 'Berlin'), (b'brandenburg', 'Brandenburg'), (b'bremen', 'Bremen'), (b'hamburg', 'Hamburg'), (b'hessen', 'Hesse'), (b'mecklenburg-vorpommern', 'Mecklenburg-Western Pomerania'), (b'niedersachsen', 'Lower Saxony'), (b'nordrhein-westfalen', 'North Rhine-Westphalia'), (b'rheinland-pfalz', 'Rhineland-Palatinate'), (b'saarland', 'Saarland'), (b'sachsen', 'Saxony'), (b'sachsen-anhalt', 'Saxony-Anhalt'), (b'schleswig-holstein', 'Schleswig-Holstein'), (b'thueringen', 'Thuringia')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fine',
            name='treasury',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fine',
            name='year',
            field=models.SmallIntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(max_length=512, db_index=True),
            preserve_default=True,
        ),
    ]
