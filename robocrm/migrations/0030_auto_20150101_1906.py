# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0029_auto_20150101_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
