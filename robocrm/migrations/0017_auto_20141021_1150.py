# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0016_auto_20141021_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=models.CharField(max_length=9, unique=True, null=True, default=None),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=models.CharField(max_length=10, unique=True, null=True, default=None),
        ),
    ]
