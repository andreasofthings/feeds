# Generated by Django 2.2.4 on 2019-09-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0007_user_delete_cascase'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='guidislink',
            field=models.BooleanField(default=False),
        ),
    ]
