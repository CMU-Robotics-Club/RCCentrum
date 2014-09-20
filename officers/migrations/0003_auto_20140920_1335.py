# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('officers', '0002_auto_20140912_2258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='officer',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='officer',
            name='order',
            field=models.PositiveIntegerField(editable=False, default=1, db_index=True),
            preserve_default=False,
        ),
    ]
