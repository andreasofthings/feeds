# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0012_feeds_feeds_ignore_ca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='ignore_ca',
            field=models.BooleanField(default=True, verbose_name='Indicates whether certificate for this feed is from a trusted CA'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feed',
            name='site',
            field=models.ForeignKey(blank=True, to='feeds.Site', null=True),
            preserve_default=True,
        ),
    ]
