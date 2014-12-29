# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('quotetron', '0006_auto_20141225_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 29, 19, 24, 16, 536939, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2014, 12, 29, 19, 24, 33, 48934, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='updater_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='updater_type',
            field=models.ForeignKey(to='contenttypes.ContentType', default=3),
            preserve_default=False,
        ),
    ]
