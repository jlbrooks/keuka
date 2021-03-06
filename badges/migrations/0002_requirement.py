# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 18:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('details', models.TextField()),
                ('sequence', models.IntegerField(default=0)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Badge')),
            ],
        ),
    ]
