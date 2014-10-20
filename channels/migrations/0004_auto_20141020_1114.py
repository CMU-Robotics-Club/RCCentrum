# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0003_auto_20141018_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='value',
            field=models.TextField(null=True),
        ),
    ]
