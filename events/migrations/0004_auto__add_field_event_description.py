# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.description'
        db.add_column('events_event', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.description'
        db.delete_column('events_event', 'description')


    models = {
        'clubs.club': {
            'Meta': {'object_name': 'Club'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'founded': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'numberOfChapter': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'numberOfMembers': ('django.db.models.fields.TextField', [], {}),
            'typeOfOrganization': ('django.db.models.fields.TextField', [], {}),
            'urlBerkeley': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'urlPersonal': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clubs.Club']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['events']