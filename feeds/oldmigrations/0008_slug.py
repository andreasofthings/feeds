# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

        dependencies = [
            ('feeds', '0007_options'),
        ]

        operations = [
            migrations.RemoveField(
                model_name='tag',
                name=b'slug',
            ),
            migrations.RemoveField(
                model_name='category',
                name=b'slug',
            ),
            migrations.RemoveField(
                model_name='category',
                name=b'parent',
            ),
            migrations.AlterField(
                model_name='category',
                name='name',
                field=models.CharField(
                    help_text=
                    b'Short descriptive name for this category.',
                    unique=True, max_length=200),
            ),
        ]
