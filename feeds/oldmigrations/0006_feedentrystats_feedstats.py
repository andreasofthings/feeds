# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0005_post_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collected', models.DateTimeField(auto_now_add=True)),
                ('feed_ok', models.IntegerField(default=0)),
                ('feed_err', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedEntryStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed', models.ForeignKey(to='feeds.Feed', to_field='id')),
                ('collected', models.DateTimeField(auto_now_add=True)),
                ('entry_ok', models.IntegerField(default=0)),
                ('entry_err', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
