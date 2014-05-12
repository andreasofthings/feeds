# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'feeds', b'0003_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'enclosure',
            name=b'post',
            field=models.ForeignKey(to=b'feeds.Post', to_field='id'),
            preserve_default=True,
        ),
    ]
