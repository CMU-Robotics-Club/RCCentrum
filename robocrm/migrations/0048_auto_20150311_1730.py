# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0047_auto_20150311_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='id',
            field=models.CharField(primary_key=True, serialize=False, max_length=10),
            preserve_default=True,
        ),
    ]
