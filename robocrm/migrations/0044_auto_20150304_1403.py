# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0043_auto_20150210_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='machines',
            field=models.ManyToManyField(blank=True, null=True, db_index=True, to='robocrm.Machine'),
            preserve_default=True,
        ),
    ]
