# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0024_robouser_dues_paid_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='dues_paid',
            field=models.DateField(auto_now_add=True, default=datetime.date(2014, 12, 26)),
            preserve_default=False,
        ),
    ]
