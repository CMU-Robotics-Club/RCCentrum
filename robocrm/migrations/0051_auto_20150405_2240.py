# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0050_machine_powered'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 4, 5, 22, 39, 51, 132027)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='machine',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 4, 5, 22, 40, 3, 195755)),
            preserve_default=False,
        ),
    ]
