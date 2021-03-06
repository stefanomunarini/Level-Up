# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-22 10:57
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_gamestate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='date_added',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gamescore',
            name='start_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gamestate',
            name='datetime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
