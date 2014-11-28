# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('officers', '0004_auto_20140920_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='officer',
            name='memo',
            field=models.CharField(null=True, max_length=80, blank=True),
            preserve_default=True,
        ),
    ]
