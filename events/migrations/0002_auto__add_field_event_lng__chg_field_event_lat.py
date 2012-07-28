# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.lng'
        db.add_column('events_event', 'lng',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=13, decimal_places=10),
                      keep_default=False)


        # Changing field 'Event.lat'
        db.alter_column('events_event', 'lat', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10))

    def backwards(self, orm):
        # Deleting field 'Event.lng'
        db.delete_column('events_event', 'lng')


        # Changing field 'Event.lat'
        db.alter_column('events_event', 'lat', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=4))

    models = {
        'clubs.club': {
            'Meta': {'object_name': 'Club'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clubs.Club']"}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['events']