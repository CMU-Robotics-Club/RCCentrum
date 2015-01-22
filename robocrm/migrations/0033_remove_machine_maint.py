# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0032_auto_20150118_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='maint',
        ),
    ]
