# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0030_auto_20150101_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='robouser',
            name='balance',
            field=models.DecimalField(decimal_places=2, help_text='Roboclub balance(currently only being used by Fridgetron)', default=0.0, max_digits=3),
            preserve_default=True,
        ),
    ]
