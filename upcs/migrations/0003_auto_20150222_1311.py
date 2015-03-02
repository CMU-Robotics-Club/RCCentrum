# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upcs', '0002_auto_20150222_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upcitem',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upcitem',
            name='upc',
            field=models.CharField(max_length=12, unique=True),
            preserve_default=True,
        ),
    ]
