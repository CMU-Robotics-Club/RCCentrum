# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0026_auto_20141226_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='dues_paid',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
