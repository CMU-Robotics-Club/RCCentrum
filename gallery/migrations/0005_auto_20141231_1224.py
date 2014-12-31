# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20141230_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=60, blank=True, null=True),
            preserve_default=True,
        ),
    ]
