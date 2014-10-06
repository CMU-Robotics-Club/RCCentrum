# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0007_robouser_magnetic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=models.CharField(blank=True, unique=True, max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=models.CharField(blank=True, unique=True, max_length=10, null=True),
        ),
    ]
