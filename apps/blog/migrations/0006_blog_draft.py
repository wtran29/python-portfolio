# Generated by Django 2.0.8 on 2019-01-15 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]