# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.advertise'
        db.add_column('events_event', 'advertise',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.advertise'
        db.delete_column('events_event', 'advertise')


    models = {
        'clubs.club': {
            'Meta': {'object_name': 'Club'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'founded': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'typeOfOrganization': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'urlPersonal': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'advertise': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clubs.Club']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Location']", 'null': 'True', 'blank': 'True'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'typeOfEvent': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'events.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['events']