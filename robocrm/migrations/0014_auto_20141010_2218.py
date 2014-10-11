# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0013_auto_20141010_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='imgurl',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='dend',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='dstart',
        ),
    ]
