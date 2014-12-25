# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotetron', '0003_auto_20141224_1137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={},
        ),
        migrations.RemoveField(
            model_name='quote',
            name='order',
        ),
        migrations.AddField(
            model_name='quote',
            name='votes',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
    ]
