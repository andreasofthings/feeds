# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

        dependencies = [
            ('feeds', '0004_website'),
        ]

        operations = [
            migrations.AddField(
                model_name='post',
                name='linkedin',
                field=models.IntegerField(default=0),
            ),
        ]
