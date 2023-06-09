# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-12 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='message',
            field=models.CharField(default='default message', max_length=500, verbose_name='Message'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deliverylocation',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='deliverylocation',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='deliveryreceiver',
            name='name',
            field=models.CharField(max_length=256, verbose_name="Receiver's Fullname"),
        ),
        migrations.AlterField(
            model_name='deliveryreceiver',
            name='phone_number',
            field=models.CharField(max_length=40, verbose_name="Receiver's phone number"),
        ),
    ]
