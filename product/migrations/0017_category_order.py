# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-22 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20181223_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
