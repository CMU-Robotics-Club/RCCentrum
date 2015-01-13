# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150113_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apirequest',
            name='meta',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
