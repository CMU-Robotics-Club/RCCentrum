# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upcs', '0005_auto_20150222_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcitem',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upcitem',
            name='name',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
