# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0008_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed', models.ForeignKey(verbose_name='Feed Subscription', to='feeds.Feed')),
                ('user', models.ForeignKey(verbose_name='User Subscription', to='feeds.Options')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='feedstats',
            name='feed_errexc',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedstats',
            name='feed_errhttp',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedstats',
            name='feed_errparse',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedstats',
            name='feed_same',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='options',
            name='subscriptions',
            field=models.ManyToManyField(to=b'feeds.Feed', through='feeds.Subscription'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='feedstats',
            name='feed_err',
        ),
    ]
