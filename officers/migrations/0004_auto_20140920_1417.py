# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('officers', '0003_auto_20140920_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='position',
            field=models.CharField(max_length=30),
        ),
    ]
