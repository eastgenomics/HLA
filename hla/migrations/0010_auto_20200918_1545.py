# Generated by Django 3.0.8 on 2020-09-18 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hla', '0009_auto_20200904_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tests',
            name='testDate',
            field=models.DateTimeField(default=datetime.datetime.now, unique=True),
        ),
    ]