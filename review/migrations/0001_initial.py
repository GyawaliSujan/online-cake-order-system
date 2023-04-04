# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-11 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import review.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rating', models.PositiveIntegerField(choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')])),
                ('photo', models.ImageField(blank=True, null=True, upload_to=review.models.get_review_image_path)),
                ('review', models.TextField()),
            ],
        ),
    ]