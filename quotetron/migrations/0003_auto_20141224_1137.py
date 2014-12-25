# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotetron', '0002_auto_20141105_0830'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='quote',
            name='order',
            field=models.PositiveIntegerField(db_index=True, editable=False, default=0),
            preserve_default=False,
        ),
    ]
