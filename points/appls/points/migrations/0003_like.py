# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('points', '0002_place_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='points.Place')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.BaseUser')),
            ],
        ),
    ]
