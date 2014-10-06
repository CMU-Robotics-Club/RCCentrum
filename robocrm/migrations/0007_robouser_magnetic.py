# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0006_auto_20141005_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='robouser',
            name='magnetic',
            field=models.CharField(max_length=9, null=True, blank=True),
            preserve_default=True,
        ),
    ]
