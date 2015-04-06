# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('original_name', models.CharField(max_length=512)),
                ('year', models.SmallIntegerField()),
                ('state', models.CharField(max_length=25, choices=[(b'baden-wuerttemberg', 'Baden-W\xfcrttemberg'), (b'bayern', 'Bavaria'), (b'berlin', 'Berlin'), (b'brandenburg', 'Brandenburg'), (b'bremen', 'Bremen'), (b'hamburg', 'Hamburg'), (b'hessen', 'Hesse'), (b'mecklenburg-vorpommern', 'Mecklenburg-Western Pomerania'), (b'niedersachsen', 'Lower Saxony'), (b'nordrhein-westfalen', 'North Rhine-Westphalia'), (b'rheinland-pfalz', 'Rhineland-Palatinate'), (b'saarland', 'Saarland'), (b'sachsen', 'Saxony'), (b'sachsen-anhalt', 'Saxony-Anhalt'), (b'schleswig-holstein', 'Schleswig-Holstein'), (b'thueringen', 'Thuringia')])),
                ('department', models.CharField(max_length=10, choices=[(b'sta', 'Prosecutor'), (b'justiz', 'Ministry of Justice'), (b'lg', 'State Court'), (b'ag', 'Local Court'), (b'olg', 'Upper State Court')])),
                ('department_detail', models.CharField(max_length=255, blank=True)),
                ('amount', models.DecimalField(max_digits=19, decimal_places=2)),
                ('amount_received', models.DecimalField(null=True, max_digits=19, decimal_places=2, blank=True)),
                ('address', models.TextField(blank=True)),
                ('file_reference', models.CharField(max_length=255, blank=True)),
                ('source_file', models.CharField(max_length=255, blank=True)),
                ('bank_details', models.TextField(blank=True)),
                ('org_details', models.TextField(blank=True)),
                ('filename', models.CharField(max_length=255)),
                ('reference_id', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('postcode', models.CharField(max_length=10, blank=True)),
            ],
            options={
                'ordering': ('-year', 'state', '-amount'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('slug', models.SlugField(max_length=255)),
                ('sum_fines', models.DecimalField(null=True, max_digits=19, decimal_places=2)),
                ('note', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fine',
            name='organisation',
            field=models.ForeignKey(related_name='fines', to='correctiv_justizgelder.Organisation'),
            preserve_default=True,
        ),
    ]
