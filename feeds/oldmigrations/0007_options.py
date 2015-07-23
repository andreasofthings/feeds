# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_feedentrystats_feedstats'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('number_initially_displayed', models.IntegerField(default=10)),
                ('number_additionally_displayed', models.IntegerField(default=5)),
                ('max_entries_saved', models.IntegerField(default=100)),
            ],
            options={
                'verbose_name_plural': b'options',
            },
            bases=(models.Model,),
        ),
    ]
