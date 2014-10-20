# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0005_auto_20141020_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
