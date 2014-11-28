# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('channels', '0007_auto_20141118_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='created',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='updated',
        ),
        migrations.AddField(
            model_name='channel',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 28, 14, 39, 45, 886067), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2014, 11, 28, 14, 39, 57, 197505)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='updater_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='updater_type',
            field=models.ForeignKey(default=3, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
    ]
