# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 23:48
from __future__ import unicode_literals

import datetime
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('badges', '0007_auto_20170624_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeEarner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_started', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('date_submitted_for_approval', models.DateField(blank=True, null=True)),
                ('date_earned', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Started'), (1, 'Needs Approval'), (2, 'Earned')])),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Badge')),
            ],
        ),
        migrations.CreateModel(
            name='BadgeUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='badgeearner',
            name='earner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.BadgeUser'),
        ),
    ]
