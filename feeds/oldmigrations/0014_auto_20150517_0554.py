# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0013_beta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name=b'created',
        ),
        migrations.RemoveField(
            model_name='post',
            name=b'date_modified',
        ),
        migrations.RemoveField(
            model_name='post',
            name=b'last_modified',
        ),
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 17, 5, 54, 46, 385802), verbose_name='last_updated', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feed',
            name='ignore_ca',
            field=models.BooleanField(default=True, verbose_name='Indicates whether CA for this certificate should be ignored'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='site',
            field=models.ForeignKey(blank=True, to='feeds.Site', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author_email',
            field=models.EmailField(max_length=254, verbose_name='author email', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(auto_now_add=True, verbose_name='pubDate'),
        ),
    ]
