# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'feeds', b'0002_enclosure_feedpostcount_post_postreadcount_taggedpost'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'category',
            name=b'parent',
            field=models.ForeignKey(to_field='id', blank=True, to=b'feeds.Category', null=True),
            preserve_default=True,
        ),
    ]
