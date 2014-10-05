# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0005_auto_20140920_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roboresource',
            name='officer',
        ),
        migrations.RemoveField(
            model_name='roboresource',
            name='user',
        ),
        migrations.DeleteModel(
            name='RoboResource',
        ),
    ]
