# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0011_auto_20141010_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robouser',
            name='tshirt_rec',
        ),
    ]
