# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-12 15:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20170212_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='total_price',
        ),
    ]
