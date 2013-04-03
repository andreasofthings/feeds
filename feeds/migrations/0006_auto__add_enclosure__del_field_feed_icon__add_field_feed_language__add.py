# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Enclosure'
        db.create_table(u'feeds_enclosure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enclosure', to=orm['feeds.Post'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('length', self.gf('django.db.models.fields.BigIntegerField')()),
            ('enclosure_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'feeds', ['Enclosure'])

        # Deleting field 'Feed.icon'
        db.delete_column(u'feeds_feed', 'icon')

        # Adding field 'Feed.language'
        db.add_column(u'feeds_feed', 'language',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True),
                      keep_default=False)

        # Adding field 'Feed.copyright'
        db.add_column(u'feeds_feed', 'copyright',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Feed.author'
        db.add_column(u'feeds_feed', 'author',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Feed.webmaster'
        db.add_column(u'feeds_feed', 'webmaster',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Feed.pubDate'
        db.add_column(u'feeds_feed', 'pubDate',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Feed.ttl'
        db.add_column(u'feeds_feed', 'ttl',
                      self.gf('django.db.models.fields.IntegerField')(default=60),
                      keep_default=False)

        # Adding M2M table for field category on 'Post'
        db.create_table(u'feeds_post_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'feeds.post'], null=False)),
            ('category', models.ForeignKey(orm[u'feeds.category'], null=False))
        ))
        db.create_unique(u'feeds_post_category', ['post_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Enclosure'
        db.delete_table(u'feeds_enclosure')

        # Adding field 'Feed.icon'
        db.add_column(u'feeds_feed', 'icon',
                      self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Feed.language'
        db.delete_column(u'feeds_feed', 'language')

        # Deleting field 'Feed.copyright'
        db.delete_column(u'feeds_feed', 'copyright')

        # Deleting field 'Feed.author'
        db.delete_column(u'feeds_feed', 'author')

        # Deleting field 'Feed.webmaster'
        db.delete_column(u'feeds_feed', 'webmaster')

        # Deleting field 'Feed.pubDate'
        db.delete_column(u'feeds_feed', 'pubDate')

        # Deleting field 'Feed.ttl'
        db.delete_column(u'feeds_feed', 'ttl')

        # Removing M2M table for field category on 'Post'
        db.delete_table('feeds_post_category')


    models = {
        u'feeds.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'feeds.enclosure': {
            'Meta': {'object_name': 'Enclosure'},
            'enclosure_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.BigIntegerField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enclosure'", 'to': u"orm['feeds.Post']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'feeds.feed': {
            'Meta': {'ordering': "('name', 'feed_url')", 'object_name': 'Feed'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'beta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'category_feeds'", 'blank': 'True', 'to': u"orm['feeds.Category']"}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'image_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pubDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'tagline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ttl': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'webmaster': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
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
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'category_posts'", 'blank': 'True', 'to': u"orm['feeds.Category']"}),
            'comments': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'has_errors': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        u'feeds.postreadcount': {
            'Meta': {'object_name': 'PostReadCount'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Post']"})
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