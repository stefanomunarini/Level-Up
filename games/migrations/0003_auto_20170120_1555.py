# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-20 15:55
from __future__ import unicode_literals

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20170119_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamescreenshot',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]