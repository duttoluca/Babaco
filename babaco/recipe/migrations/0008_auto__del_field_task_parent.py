# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Task.parent'
        db.delete_column('recipe_task', 'parent_id')

        # Adding M2M table for field parents on 'Task'
        db.create_table('recipe_task_parents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_task', models.ForeignKey(orm['recipe.task'], null=False)),
            ('to_task', models.ForeignKey(orm['recipe.task'], null=False))
        ))
        db.create_unique('recipe_task_parents', ['from_task_id', 'to_task_id'])


    def backwards(self, orm):
        
        # Adding field 'Task.parent'
        db.add_column('recipe_task', 'parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Task'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field parents on 'Task'
        db.delete_table('recipe_task_parents')


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
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parents_rel_+'", 'null': 'True', 'to': "orm['recipe.Task']"}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipe.Recipe']"}),
            'startTime': ('django.db.models.fields.IntegerField', [], {}),
            'stopTime': ('django.db.models.fields.IntegerField', [], {}),
            'time_needed': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['recipe']
