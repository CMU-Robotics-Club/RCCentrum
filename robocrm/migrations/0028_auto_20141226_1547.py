# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0027_auto_20141226_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='dues_paid',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
