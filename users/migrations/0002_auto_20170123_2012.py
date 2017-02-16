# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 20:12
from __future__ import unicode_literals

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, default='image/upload/v1485194129/default/Ninja-icon.jpg', max_length=255, null=True, verbose_name='Profile picture'),
        ),
    ]