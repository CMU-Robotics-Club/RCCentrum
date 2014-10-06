# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0008_auto_20141006_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=models.CharField(unique=True, null=True, max_length=9),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=models.CharField(unique=True, null=True, max_length=10),
        ),
    ]
