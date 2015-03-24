# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0048_auto_20150311_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='rfid_present',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='machine',
            name='user',
            field=models.ForeignKey(null=True, to='robocrm.RoboUser'),
            preserve_default=True,
        ),
    ]
