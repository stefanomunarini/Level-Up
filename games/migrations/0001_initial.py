# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-16 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import games.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(unique=True)),
                ('url', models.URLField()),
                ('icon', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('is_public', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('dev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='users.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='GameScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='games.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='users.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='GameScreenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=255, upload_to=games.models.get_upload_path)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='games.Game')),
            ],
        ),
    ]
