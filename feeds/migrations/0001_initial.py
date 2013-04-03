# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'feeds_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('relevant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('touched', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'feeds', ['Tag'])

        # Adding model 'Category'
        db.create_table(u'feeds_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'feeds', ['Category'])

        # Adding model 'Feed'
        db.create_table(u'feeds_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('beta', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('tagline', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('image_title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('image_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('etag', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feeds', ['Feed'])

        # Adding M2M table for field category on 'Feed'
        db.create_table(u'feeds_feed_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm[u'feeds.feed'], null=False)),
            ('category', models.ForeignKey(orm[u'feeds.category'], null=False))
        ))
        db.create_unique(u'feeds_feed_category', ['feed_id', 'category_id'])

        # Adding model 'FeedPostCount'
        db.create_table(u'feeds_feedpostcount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Feed'])),
            ('entry_new', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('entry_updated', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('entry_same', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('entry_err', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'feeds', ['FeedPostCount'])

        # Adding model 'Post'
        db.create_table(u'feeds_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('author_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('comments', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tweets', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blogs', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('plus1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('likes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('shares', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pageviews', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_social', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('was_announced', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('was_recommended', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'feeds', ['Post'])

        # Adding model 'TaggedPost'
        db.create_table(u'feeds_taggedpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_tags', to=orm['feeds.Tag'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Post'])),
        ))
        db.send_create_signal(u'feeds', ['TaggedPost'])

        # Adding unique constraint on 'TaggedPost', fields ['tag', 'post']
        db.create_unique(u'feeds_taggedpost', ['tag_id', 'post_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TaggedPost', fields ['tag', 'post']
        db.delete_unique(u'feeds_taggedpost', ['tag_id', 'post_id'])

        # Deleting model 'Tag'
        db.delete_table(u'feeds_tag')

        # Deleting model 'Category'
        db.delete_table(u'feeds_category')

        # Deleting model 'Feed'
        db.delete_table(u'feeds_feed')

        # Removing M2M table for field category on 'Feed'
        db.delete_table('feeds_feed_category')

        # Deleting model 'FeedPostCount'
        db.delete_table(u'feeds_feedpostcount')

        # Deleting model 'Post'
        db.delete_table(u'feeds_post')

        # Deleting model 'TaggedPost'
        db.delete_table(u'feeds_taggedpost')


    models = {
        u'feeds.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'feeds.feed': {
            'Meta': {'ordering': "('name', 'feed_url')", 'object_name': 'Feed'},
            'beta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'category_feeds'", 'symmetrical': 'False', 'to': u"orm['feeds.Category']"}),
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'image_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tagline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'feeds.feedpostcount': {
            'Meta': {'object_name': 'FeedPostCount'},
            'created': ('django.db.models.fields.IntegerField', [], {}),
            'entry_err': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entry_new': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entry_same': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entry_updated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'feeds.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'blogs': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'pageviews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'plus1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tag_posts'", 'symmetrical': 'False', 'through': u"orm['feeds.TaggedPost']", 'to': u"orm['feeds.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'tweets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_social': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'was_announced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'was_recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'feeds.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'relevant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'touched': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'feeds.taggedpost': {
            'Meta': {'unique_together': "(('tag', 'post'),)", 'object_name': 'TaggedPost'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Post']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_tags'", 'to': u"orm['feeds.Tag']"})
        }
    }

    complete_apps = ['feeds']