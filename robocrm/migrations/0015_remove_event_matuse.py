# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0014_auto_20141010_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='matuse',
        ),
    ]
