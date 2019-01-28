# Generated by Django 2.1.5 on 2019-01-28 09:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250), blank=True, default=list, size=None),
        ),
    ]
