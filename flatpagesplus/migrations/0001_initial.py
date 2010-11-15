# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MainFlatPage'
        db.create_table('flatpagesplus_mainflatpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('embedded_head_content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('embedded_foot_content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('registration_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('flatpagesplus', ['MainFlatPage'])

        # Adding M2M table for field sites on 'MainFlatPage'
        db.create_table('flatpagesplus_mainflatpage_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mainflatpage', models.ForeignKey(orm['flatpagesplus.mainflatpage'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('flatpagesplus_mainflatpage_sites', ['mainflatpage_id', 'site_id'])

        # Adding model 'SubFlatPage'
        db.create_table('flatpagesplus_subflatpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flatpagesplus.MainFlatPage'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('insert_link', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('flatpagesplus', ['SubFlatPage'])

        # Adding unique constraint on 'SubFlatPage', fields ['parent', 'type']
        db.create_unique('flatpagesplus_subflatpage', ['parent_id', 'type'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'SubFlatPage', fields ['parent', 'type']
        db.delete_unique('flatpagesplus_subflatpage', ['parent_id', 'type'])

        # Deleting model 'MainFlatPage'
        db.delete_table('flatpagesplus_mainflatpage')

        # Removing M2M table for field sites on 'MainFlatPage'
        db.delete_table('flatpagesplus_mainflatpage_sites')

        # Deleting model 'SubFlatPage'
        db.delete_table('flatpagesplus_subflatpage')


    models = {
        'flatpagesplus.mainflatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'MainFlatPage'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'embedded_foot_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'embedded_head_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'flatpagesplus.subflatpage': {
            'Meta': {'unique_together': "(('parent', 'type'),)", 'object_name': 'SubFlatPage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insert_link': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flatpagesplus.MainFlatPage']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['flatpagesplus']
