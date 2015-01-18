# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0031_robouser_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='balance',
            field=models.DecimalField(default=0.0, max_digits=5, help_text='Roboclub balance(currently only being used by Fridgetron)', decimal_places=2),
            preserve_default=True,
        ),
    ]
