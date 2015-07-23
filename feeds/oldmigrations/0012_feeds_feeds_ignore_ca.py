from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0011_feeds_feedentrystats_entry_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='ignore_ca',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
