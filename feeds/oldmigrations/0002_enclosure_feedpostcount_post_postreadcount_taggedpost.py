# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'feeds', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'FeedPostCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'feed', models.ForeignKey(to=b'feeds.Feed', to_field='id', verbose_name='feed')),
                (b'entry_new', models.IntegerField(default=0)),
                (b'entry_updated', models.IntegerField(default=0)),
                (b'entry_same', models.IntegerField(default=0)),
                (b'entry_err', models.IntegerField(default=0)),
                (b'created', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Enclosure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'url', models.URLField()),
                (b'length', models.BigIntegerField()),
                (b'enclosure_type', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'feed', models.ForeignKey(to=b'feeds.Feed', to_field='id', verbose_name='feed')),
                (b'title', models.CharField(max_length=512)),
                (b'link', models.URLField(verbose_name='link')),
                (b'content', models.TextField(verbose_name='description', blank=True)),
                (b'author', models.CharField(max_length=50, verbose_name='author', blank=True)),
                (b'author_email', models.EmailField(max_length=75, verbose_name='author email', blank=True)),
                (b'comments', models.URLField(verbose_name='comments', blank=True)),
                (b'guid', models.CharField(unique=True, max_length=255, verbose_name='guid', db_index=True)),
                (b'created', models.DateTimeField(auto_now_add=True, verbose_name='pubDate')),
                (b'published', models.BooleanField(default=False)),
                (b'last_modified', models.DateTimeField(null=True, blank=True)),
                (b'date_modified', models.DateTimeField(null=True, verbose_name='date modified', blank=True)),
                (b'tweets', models.IntegerField(default=0)),
                (b'blogs', models.IntegerField(default=0)),
                (b'plus1', models.IntegerField(default=0)),
                (b'likes', models.IntegerField(default=0)),
                (b'shares', models.IntegerField(default=0)),
                (b'pageviews', models.IntegerField(default=0)),
                (b'score', models.IntegerField(default=0)),
                (b'updated_social', models.BooleanField(default=False)),
                (b'was_announced', models.BooleanField(default=False)),
                (b'was_recommended', models.BooleanField(default=False)),
                (b'has_errors', models.BooleanField(default=True)),
                (b'category', models.ManyToManyField(to=b'feeds.Category', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'PostReadCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'post', models.ForeignKey(to=b'feeds.Post', to_field='id')),
                (b'created', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'TaggedPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'tag', models.ForeignKey(to=b'feeds.Tag', to_field='id', verbose_name='tag')),
                (b'post', models.ForeignKey(to=b'feeds.Post', to_field='id', verbose_name='post')),
            ],
            options={
                'unique_together': set([(b'tag', b'post')]),
                'verbose_name': 'tagged item',
                'verbose_name_plural': 'tagged node',
            },
            bases=(models.Model,),
        ),
    ]
