# Generated by Django 2.2.4 on 2019-10-02 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0009_auto_20190927_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='etag',
            field=models.CharField(blank=True, max_length=256, verbose_name='etag'),
        ),
    ]
