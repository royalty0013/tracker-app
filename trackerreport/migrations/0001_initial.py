# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-12 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_name', models.CharField(max_length=50)),
                ('distance_covered', models.CharField(max_length=50)),
                ('fuel_consumption', models.CharField(max_length=50)),
                ('fuel_allocated', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('distance_allocated', models.CharField(blank=True, max_length=100, null=True)),
                ('fuel_per_km', models.CharField(blank=True, max_length=100, null=True)),
                ('top_speed', models.CharField(blank=True, max_length=50, null=True)),
                ('move_duration', models.CharField(blank=True, max_length=100, null=True)),
                ('stop_duration', models.CharField(blank=True, max_length=100, null=True)),
                ('move_at', models.CharField(blank=True, max_length=100, null=True)),
                ('overspeed', models.CharField(blank=True, max_length=100, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Vehicle Report',
                'verbose_name_plural': 'Vehicle Reports',
            },
        ),
    ]
