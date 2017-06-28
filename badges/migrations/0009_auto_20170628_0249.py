# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0008_auto_20170626_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgeearner',
            name='status',
            field=models.IntegerField(choices=[(0, 'Started'), (1, 'Needs Approval'), (2, 'Earned')], default=0),
        ),
        migrations.AlterUniqueTogether(
            name='badgeearner',
            unique_together=set([('earner', 'badge')]),
        ),
    ]
