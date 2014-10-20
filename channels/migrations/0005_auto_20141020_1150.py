# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0004_auto_20141020_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='value',
            field=models.TextField(null=True, blank=True),
        ),
    ]
