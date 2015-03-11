# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0045_machine_toolbox_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='toolbox_id',
            field=models.PositiveIntegerField(default=None, blank=True, null=True, unique=True),
            preserve_default=True,
        ),
    ]
