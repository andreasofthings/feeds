# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'feeds', b'0004_enclosure_post'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'post',
            name=b'tags',
            field=models.ManyToManyField(to=b'feeds.Tag', through=b'feeds.TaggedPost'),
            preserve_default=True,
        ),
    ]
