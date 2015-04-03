# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organisation'
        db.create_table(u'correctiv_justizgelder_organisation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('sum_fines', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'correctiv_justizgelder', ['Organisation'])

        # Adding model 'Fine'
        db.create_table(u'correctiv_justizgelder_fine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organisation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fines', to=orm['correctiv_justizgelder.Organisation'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('original_name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('department_detail', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2)),
            ('amount_received', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file_reference', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_file', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('bank_details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('org_details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reference_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
        ))
        db.send_create_signal(u'correctiv_justizgelder', ['Fine'])


    def backwards(self, orm):
        # Deleting model 'Organisation'
        db.delete_table(u'correctiv_justizgelder_organisation')

        # Deleting model 'Fine'
        db.delete_table(u'correctiv_justizgelder_fine')


    models = {
        u'correctiv_justizgelder.fine': {
            'Meta': {'ordering': "('-year', 'state', '-amount')", 'object_name': 'Fine'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'amount_received': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'bank_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'department_detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'file_reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'org_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fines'", 'to': u"orm['correctiv_justizgelder.Organisation']"}),
            'original_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'reference_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_file': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'correctiv_justizgelder.organisation': {
            'Meta': {'object_name': 'Organisation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'sum_fines': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2'})
        }
    }

    complete_apps = ['correctiv_justizgelder']