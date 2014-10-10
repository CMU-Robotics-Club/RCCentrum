# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0012_remove_robouser_tshirt_rec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robouser',
            name='bench_status',
        ),
        migrations.RemoveField(
            model_name='robouser',
            name='shop_status',
        ),
    ]
