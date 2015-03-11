# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0046_auto_20150311_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='id',
            field=models.CharField(max_length=10, editable=False, primary_key=True, serialize=False),
            preserve_default=True,
        ),
    ]
