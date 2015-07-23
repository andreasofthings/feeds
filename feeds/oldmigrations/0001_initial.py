# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'url', models.URLField(unique=True)),
                (b'slug', models.SlugField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=50, verbose_name='name', db_index=True)),
                (b'slug', models.SlugField(help_text=b'Short descriptive unique name for use in urls.', unique=True, max_length=255)),
                (b'relevant', models.BooleanField(default=False)),
                (b'touched', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': (b'name',),
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(help_text=b'Short descriptive name for this category.', max_length=200)),
                (b'slug', models.SlugField(help_text=b'Short descriptive unique name for use in urls.', unique=True, max_length=255)),
            ],
            options={
                'ordering': (b'name',),
                'verbose_name': b'category',
                'verbose_name_plural': b'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'site', models.ForeignKey(to=b'feeds.Site', to_field='id', null=True)),
                (b'feed_url', models.URLField(unique=True, verbose_name='feed url')),
                (b'name', models.CharField(max_length=100, null=True, verbose_name='name', blank=True)),
                (b'short_name', models.CharField(max_length=50, null=True, verbose_name='short_name', blank=True)),
                (b'slug', models.SlugField(null=True, max_length=255, blank=True, help_text=b'Short descriptive unique name for use in urls.', unique=True)),
                (b'is_active', models.BooleanField(default=True, help_text='If disabled, this feed will not be further updated.', verbose_name='is active')),
                (b'beta', models.BooleanField(default=False, help_text='If beta, celery pipeline.', verbose_name='is beta')),
                (b'has_no_guid', models.BooleanField(default=False, help_text="\n                    This feed doesn't have a proper guid.\n                    Use something else instead.\n                    ", verbose_name='has no guid')),
                (b'title', models.CharField(max_length=200, verbose_name='title', blank=True)),
                (b'link', models.URLField(verbose_name='link', blank=True)),
                (b'tagline', models.TextField(help_text='Phrase or sentence describing the channel.', verbose_name='description', blank=True)),
                (b'language', models.CharField(max_length=8, verbose_name='language', blank=True)),
                (b'copyright', models.CharField(max_length=64, verbose_name='copyright', blank=True)),
                (b'author', models.CharField(max_length=64, verbose_name='managingEditor', blank=True)),
                (b'webmaster', models.CharField(max_length=64, verbose_name='webmaster', blank=True)),
                (b'pubDate', models.DateTimeField(null=True, verbose_name='pubDate', blank=True)),
                (b'last_modified', models.DateTimeField(null=True, verbose_name='lastBuildDate', blank=True)),
                (b'ttl', models.IntegerField(default=60, verbose_name="\n          TTL stands for time to live.\n          It's a number of minutes that indicates how long a\n          channel can be cached before refreshing from the source.\n          ")),
                (b'image_title', models.CharField(max_length=200, verbose_name='image_title', blank=True)),
                (b'image_link', models.URLField(verbose_name='image_link', blank=True)),
                (b'image_url', models.URLField(verbose_name='image_url', blank=True)),
                (b'etag', models.CharField(max_length=50, verbose_name='etag', blank=True)),
                (b'last_checked', models.DateTimeField(null=True, verbose_name='last checked', blank=True)),
                (b'announce_posts', models.BooleanField(default=False)),
                (b'category', models.ManyToManyField(to=b'feeds.Category', blank=True)),
            ],
            options={
                'ordering': (b'name', b'feed_url'),
                'verbose_name': 'feed',
                'verbose_name_plural': 'feeds',
                'permissions': ((b'can_refresh_feed', b'Can refresh feed'),),
            },
            bases=(models.Model,),
        ),
    ]
