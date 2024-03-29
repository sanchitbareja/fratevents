# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('events_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
        ))
        db.send_create_signal('events', ['Location'])

        # Deleting field 'Event.lat'
        db.delete_column('events_event', 'lat')

        # Deleting field 'Event.lng'
        db.delete_column('events_event', 'lng')

        # Adding field 'Event.location'
        db.add_column('events_event', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Location'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Event.description'
        db.alter_column('events_event', 'description', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table('events_location')


        # User chose to not deal with backwards NULL issues for 'Event.lat'
        raise RuntimeError("Cannot reverse this migration. 'Event.lat' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Event.lng'
        raise RuntimeError("Cannot reverse this migration. 'Event.lng' and its values cannot be restored.")
        # Deleting field 'Event.location'
        db.delete_column('events_event', 'location_id')


        # Changing field 'Event.description'
        db.alter_column('events_event', 'description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))

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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Location']", 'null': 'True', 'blank': 'True'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '300'})
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