# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


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
                ('slug', models.SlugField()),
                ('url', models.URLField()),
                ('icon', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('is_public', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=True)),
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
                ('image', models.ImageField(upload_to='')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='games.Game')),
            ],
        ),
    ]