# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-20 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='tech',
        ),
        migrations.AlterField(
            model_name='work',
            name='image',
            field=models.ImageField(blank=True, upload_to=b'images/'),
        ),
    ]
