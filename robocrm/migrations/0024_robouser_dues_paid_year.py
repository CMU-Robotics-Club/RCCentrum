# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0023_auto_20141120_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='robouser',
            name='dues_paid_year',
            field=models.BooleanField(default=True, help_text='Uncheck if only Semester membership was paid'),
            preserve_default=True,
        ),
    ]
