# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0015_remove_event_matuse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=models.CharField(max_length=9, unique=True, default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=models.CharField(max_length=10, unique=True, default=None, null=True, blank=True),
        ),
    ]
