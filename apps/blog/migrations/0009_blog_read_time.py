# Generated by Django 2.0.8 on 2019-01-17 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190115_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
