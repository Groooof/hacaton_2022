# Generated by Django 3.2.13 on 2022-05-15 04:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0006_auto_20220515_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='refresh_destroy_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 14, 4, 1, 13, 652387)),
        ),
    ]