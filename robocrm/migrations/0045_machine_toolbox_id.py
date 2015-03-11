# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0044_auto_20150304_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='toolbox_id',
            field=models.PositiveIntegerField(blank=True, null=True, default=None),
            preserve_default=True,
        ),
    ]
