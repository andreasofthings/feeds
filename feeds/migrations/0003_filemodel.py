# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_errors'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.FileField(upload_to=b'', verbose_name='data')),
            ],
        ),
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ('name', 'feed_url'), 'verbose_name': 'feed', 'verbose_name_plural': 'feeds', 'permissions': (('can_refresh_feed', 'Can refresh feed'), ('can_subscribe_feed', 'Can subscribe to feed'), ('can_backup_feed', 'Can backup feeds'))},
        ),
        migrations.AlterField(
            model_name='options',
            name='number_additionally_displayed',
            field=models.IntegerField(default=5, help_text='ToDo'),
        ),
        migrations.AlterField(
            model_name='options',
            name='number_initially_displayed',
            field=models.IntegerField(default=10, help_text='Paginate by'),
        ),
        migrations.AlterField(
            model_name='options',
            name='user',
            field=models.ForeignKey(help_text='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
