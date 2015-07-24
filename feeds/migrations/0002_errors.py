# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='has_no_guid',
        ),
        migrations.AddField(
            model_name='feed',
            name='errors',
            field=models.IntegerField(default=0, help_text="\n                    Remember errors for a feed, and don't try again if a\n                    threshold is met\n                    ", verbose_name='Has errors'),
        ),
    ]
