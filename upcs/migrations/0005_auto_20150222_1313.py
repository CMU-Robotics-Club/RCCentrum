# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upcs', '0004_auto_20150222_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upcitem',
            name='name',
            field=models.CharField(editable=False, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upcitem',
            name='upc',
            field=models.CharField(editable=False, unique=True, max_length=12),
            preserve_default=True,
        ),
    ]
