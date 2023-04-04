# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-05-06 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_cake_best_selling'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Holiday Date')),
                ('remark', models.CharField(max_length=100, verbose_name='Remarks')),
            ],
        ),
        migrations.AlterField(
            model_name='checkout',
            name='message',
            field=models.CharField(max_length=500, verbose_name='Remarks'),
        ),
    ]
