# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Task.time'
        db.delete_column('recipe_task', 'time')

        # Deleting field 'Task.attention'
        db.delete_column('recipe_task', 'attention')

        # Adding field 'Task.description'
        db.add_column('recipe_task', 'description', self.gf('django.db.models.fields.TextField')(default='', max_length=4000, blank=True), keep_default=False)

        # Adding field 'Task.time_needed'
        db.add_column('recipe_task', 'time_needed', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Task.attention_needed'
        db.add_column('recipe_task', 'attention_needed', self.gf('django.db.models.fields.IntegerField')(default=10), keep_default=False)

        # Adding field 'Task.ins_date'
        db.add_column('recipe_task', 'ins_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2012, 3, 23), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Task.time'
        db.add_column('recipe_task', 'time', self.gf('django.db.models.fields.IntegerField')(default=datetime.date(2012, 3, 23)), keep_default=False)

        # Adding field 'Task.attention'
        db.add_column('recipe_task', 'attention', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Deleting field 'Task.description'
        db.delete_column('recipe_task', 'description')

        # Deleting field 'Task.time_needed'
        db.delete_column('recipe_task', 'time_needed')

        # Deleting field 'Task.attention_needed'
        db.delete_column('recipe_task', 'attention_needed')

        # Deleting field 'Task.ins_date'
        db.delete_column('recipe_task', 'ins_date')


    models = {
        'recipe.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '4000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ins_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'recipe.task': {
            'Meta': {'object_name': 'Task'},
            'attention_needed': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '4000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ins_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipe.Task']", 'null': 'True', 'blank': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipe.Recipe']"}),
            'startTime': ('django.db.models.fields.IntegerField', [], {}),
            'stopTime': ('django.db.models.fields.IntegerField', [], {}),
            'time_needed': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['recipe']
