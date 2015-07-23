# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0009_auto_20140904_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='check_interval',
            field=models.IntegerField(default=5, verbose_name='Interval in Minutes between checks.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='enclosure',
            name=b'post',
            field=models.ForeignKey(related_name=b'enclosure', to='feeds.Post'),
        ),
        migrations.AlterField(
            model_name='feed',
            name=b'category',
            field=models.ManyToManyField(related_name=b'category_feeds', to=b'feeds.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name=b'category',
            field=models.ManyToManyField(related_name=b'category_posts', to=b'feeds.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name=b'feed',
            field=models.ForeignKey(related_name=b'posts', verbose_name='feed', to='feeds.Feed'),
        ),
        migrations.AlterField(
            model_name='post',
            name=b'tags',
            field=models.ManyToManyField(related_name=b'tag_posts', through='feeds.TaggedPost', to=b'feeds.Tag'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='feed',
            field=models.ForeignKey(related_name=b'feed_subscription', verbose_name='Feed Subscription', to='feeds.Feed'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(related_name=b'user_subscription', verbose_name='User Subscription', to='feeds.Options'),
        ),
        migrations.AlterField(
            model_name='taggedpost',
            name=b'tag',
            field=models.ForeignKey(related_name=b'post_tags', verbose_name='tag', to='feeds.Tag'),
        ),
    ]
