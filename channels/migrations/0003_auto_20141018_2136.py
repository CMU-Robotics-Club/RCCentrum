# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0002_auto_20141016_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
        ),
    ]
