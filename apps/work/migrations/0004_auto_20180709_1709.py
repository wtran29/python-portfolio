# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-10 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0003_auto_20180709_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='video',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
