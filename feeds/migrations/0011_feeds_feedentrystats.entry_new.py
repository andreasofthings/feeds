# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0010_auto_20140923_1214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedentrystats',
            old_name='entry_ok',
            new_name='entry_new',
        ),
        migrations.AddField(
            model_name='feedentrystats',
            name='entry_same',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedentrystats',
            name='entry_updated',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feed',
            name=b'last_checked',
            field=models.DateTimeField(auto_now=True, verbose_name='last checked', null=True),
            preserve_default=True,
        ),
    ]
