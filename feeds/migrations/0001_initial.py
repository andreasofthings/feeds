# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Short descriptive name for this category.', unique=True, max_length=200)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_url', models.URLField(unique=True, verbose_name='feed url')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='name', blank=True)),
                ('short_name', models.CharField(max_length=50, null=True, verbose_name='short_name', blank=True)),
                ('slug', models.SlugField(null=True, max_length=255, blank=True, help_text=b'Short descriptive unique name for use in urls.', unique=True)),
                ('is_active', models.BooleanField(default=True, help_text='If disabled, this feed will not be further updated.', verbose_name='is active')),
                ('has_no_guid', models.BooleanField(default=False, help_text="\n                    This feed doesn't have a proper guid.\n                    Use something else instead.\n                    ", verbose_name='has no guid')),
                ('title', models.CharField(max_length=200, verbose_name='title', blank=True)),
                ('link', models.URLField(verbose_name='link', blank=True)),
                ('tagline', models.TextField(help_text='Phrase or sentence describing the channel.', verbose_name='description', blank=True)),
                ('language', models.CharField(max_length=8, verbose_name='language', blank=True)),
                ('copyright', models.CharField(max_length=64, verbose_name='copyright', blank=True)),
                ('author', models.CharField(max_length=64, verbose_name='managingEditor', blank=True)),
                ('webmaster', models.CharField(max_length=64, verbose_name='webmaster', blank=True)),
                ('pubDate', models.DateTimeField(null=True, verbose_name='pubDate', blank=True)),
                ('last_modified', models.DateTimeField(null=True, verbose_name='lastBuildDate', blank=True)),
                ('ttl', models.IntegerField(default=60, verbose_name="\n          TTL stands for time to live.\n          It's a number of minutes that indicates how long a\n          channel can be cached before refreshing from the source.\n          ")),
                ('image_title', models.CharField(max_length=200, verbose_name='image_title', blank=True)),
                ('image_link', models.URLField(verbose_name='image_link', blank=True)),
                ('image_url', models.URLField(verbose_name='image_url', blank=True)),
                ('etag', models.CharField(max_length=50, verbose_name='etag', blank=True)),
                ('last_checked', models.DateTimeField(auto_now=True, verbose_name='last checked', null=True)),
                ('check_interval', models.IntegerField(default=5, verbose_name='Interval in Minutes between checks.')),
                ('ignore_ca', models.BooleanField(default=True, verbose_name='Indicates whether CA for this certificate should be ignored')),
                ('announce_posts', models.BooleanField(default=False)),
                ('category', models.ManyToManyField(related_name='category_feeds', to='feeds.Category', blank=True)),
            ],
            options={
                'ordering': ('name', 'feed_url'),
                'verbose_name': 'feed',
                'verbose_name_plural': 'feeds',
                'permissions': (
                    ('can_refresh_feed', 'Can refresh feed'),
                    ('can_subscribe_feed', 'Can subscribe feed'),
                    ('can_backup_feed', 'Can backup feed'),
                ),
            },
        ),
        migrations.CreateModel(
            name='FeedEntryStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collected', models.DateTimeField(auto_now_add=True)),
                ('entry_new', models.IntegerField(default=0)),
                ('entry_same', models.IntegerField(default=0)),
                ('entry_updated', models.IntegerField(default=0)),
                ('entry_err', models.IntegerField(default=0)),
                ('feed', models.ForeignKey(to='feeds.Feed')),
            ],
        ),
        migrations.CreateModel(
            name='FeedPostCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_new', models.IntegerField(default=0)),
                ('entry_updated', models.IntegerField(default=0)),
                ('entry_same', models.IntegerField(default=0)),
                ('entry_err', models.IntegerField(default=0)),
                ('created', models.IntegerField()),
                ('feed', models.ForeignKey(verbose_name='feed', to='feeds.Feed')),
            ],
        ),
        migrations.CreateModel(
            name='FeedStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collected', models.DateTimeField(auto_now_add=True)),
                ('feed_ok', models.IntegerField(default=0)),
                ('feed_same', models.IntegerField(default=0)),
                ('feed_errparse', models.IntegerField(default=0)),
                ('feed_errhttp', models.IntegerField(default=0)),
                ('feed_errexc', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_initially_displayed', models.IntegerField(default=10)),
                ('number_additionally_displayed', models.IntegerField(default=5)),
                ('max_entries_saved', models.IntegerField(default=100)),
            ],
            options={
                'verbose_name_plural': 'options',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('link', models.URLField(verbose_name='link')),
                ('content', models.TextField(verbose_name='description', blank=True)),
                ('author', models.CharField(max_length=50, verbose_name='author', blank=True)),
                ('author_email', models.EmailField(max_length=254, verbose_name='author email', blank=True)),
                ('comments', models.URLField(verbose_name='comments', blank=True)),
                ('guid', models.CharField(unique=True, max_length=255, verbose_name='guid', db_index=True)),
                ('published', models.DateTimeField(verbose_name='pubDate')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='last_updated')),
                ('tweets', models.IntegerField(default=0)),
                ('blogs', models.IntegerField(default=0)),
                ('plus1', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('pageviews', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('updated_social', models.BooleanField(default=False)),
                ('was_announced', models.BooleanField(default=False)),
                ('was_recommended', models.BooleanField(default=False)),
                ('has_errors', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(related_name='category_posts', to='feeds.Category', blank=True)),
                ('feed', models.ForeignKey(related_name='posts', verbose_name='feed', to='feeds.Feed')),
            ],
        ),
        migrations.CreateModel(
            name='PostReadCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='feeds.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(unique=True)),
                ('slug', models.SlugField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed', models.ForeignKey(related_name='feed_subscription', verbose_name='Feed Subscription', to='feeds.Feed')),
                ('user', models.ForeignKey(related_name='user_subscription', verbose_name='User Subscription', to='feeds.Options')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name', db_index=True)),
                ('relevant', models.BooleanField(default=False)),
                ('touched', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.ForeignKey(verbose_name='post', to='feeds.Post')),
                ('tag', models.ForeignKey(related_name='post_tags', verbose_name='tag', to='feeds.Tag')),
            ],
            options={
                'verbose_name': 'tagged item',
                'verbose_name_plural': 'tagged node',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='tag_posts', through='feeds.TaggedPost', to='feeds.Tag'),
        ),
        migrations.AddField(
            model_name='options',
            name='subscriptions',
            field=models.ManyToManyField(to='feeds.Feed', through='feeds.Subscription'),
        ),
        migrations.AddField(
            model_name='options',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feed',
            name='site',
            field=models.ForeignKey(blank=True, to='feeds.Site', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='taggedpost',
            unique_together=set([('tag', 'post')]),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('user', 'feed')]),
        ),
    ]
