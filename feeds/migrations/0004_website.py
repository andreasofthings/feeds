# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_filemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text='URL of the Website.', unique=True)),
                ('slug', models.SlugField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='feed',
            name='site',
        ),
        migrations.DeleteModel(
            name='Site',
        ),
        migrations.AddField(
            model_name='feed',
            name='website',
            field=models.ForeignKey(blank=True, to='feeds.WebSite', null=True),
        ),
    ]
