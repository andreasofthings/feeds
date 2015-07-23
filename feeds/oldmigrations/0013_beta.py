# encoding: utf8
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

        dependencies = [
            ('feeds', '0012_feeds_feeds_ignore_ca'),
        ]

        operations = [
            migrations.RemoveField(
                model_name='feed',
                name=b'beta',
            ),
        ]
