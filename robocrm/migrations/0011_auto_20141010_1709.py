# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0010_remove_robouser_club_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=models.CharField(max_length=9, null=True, blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=models.CharField(max_length=10, null=True, blank=True, unique=True),
        ),
    ]
