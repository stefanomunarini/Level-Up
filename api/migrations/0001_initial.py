# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 20:12
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20170123_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=36, unique=True)),
                ('website_url', models.URLField(verbose_name='The website in where you will use this token')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_tokens', to='users.UserProfile')),
            ],
        ),
    ]
