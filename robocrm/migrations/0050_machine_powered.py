# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0049_auto_20150324_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='powered',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
