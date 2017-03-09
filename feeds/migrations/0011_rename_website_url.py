# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0010_fix_related_name'),
    ]

    operations = [
        migrations.RenameField('website', 'url', 'website_url'),
    ]
