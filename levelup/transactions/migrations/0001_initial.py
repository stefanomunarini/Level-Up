# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0.0)),
                ('status', models.CharField(choices=[('success', 'Success'), ('cancel', 'Cancel'), ('error', 'Error')], max_length=16)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='games.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='users.UserProfile')),
            ],
        ),
    ]
