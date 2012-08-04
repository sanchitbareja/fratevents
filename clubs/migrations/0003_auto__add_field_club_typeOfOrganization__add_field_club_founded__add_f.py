# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Club.typeOfOrganization'
        db.add_column('clubs_club', 'typeOfOrganization',
                      self.gf('django.db.models.fields.TextField')(default=' '),
                      keep_default=False)

        # Adding field 'Club.founded'
        db.add_column('clubs_club', 'founded',
                      self.gf('django.db.models.fields.TextField')(default=' '),
                      keep_default=False)

        # Adding field 'Club.numberOfChapter'
        db.add_column('clubs_club', 'numberOfChapter',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Club.numberOfMembers'
        db.add_column('clubs_club', 'numberOfMembers',
                      self.gf('django.db.models.fields.TextField')(default=' '),
                      keep_default=False)

        # Adding field 'Club.urlPersonal'
        db.add_column('clubs_club', 'urlPersonal',
                      self.gf('django.db.models.fields.URLField')(default=' ', max_length=200),
                      keep_default=False)

        # Adding field 'Club.urlBerkeley'
        db.add_column('clubs_club', 'urlBerkeley',
                      self.gf('django.db.models.fields.URLField')(default=' ', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Club.typeOfOrganization'
        db.delete_column('clubs_club', 'typeOfOrganization')

        # Deleting field 'Club.founded'
        db.delete_column('clubs_club', 'founded')

        # Deleting field 'Club.numberOfChapter'
        db.delete_column('clubs_club', 'numberOfChapter')

        # Deleting field 'Club.numberOfMembers'
        db.delete_column('clubs_club', 'numberOfMembers')

        # Deleting field 'Club.urlPersonal'
        db.delete_column('clubs_club', 'urlPersonal')

        # Deleting field 'Club.urlBerkeley'
        db.delete_column('clubs_club', 'urlBerkeley')


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
        }
    }

    complete_apps = ['clubs']