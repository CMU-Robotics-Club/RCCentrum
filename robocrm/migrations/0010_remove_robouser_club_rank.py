# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0009_auto_20141006_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robouser',
            name='club_rank',
        ),
    ]
