# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0022_auto_20141027_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='major',
            field=models.CharField(max_length=50),
        ),
    ]
