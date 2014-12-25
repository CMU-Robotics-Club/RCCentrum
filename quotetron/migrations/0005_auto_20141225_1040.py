# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotetron', '0004_auto_20141224_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='votes',
        ),
        migrations.AddField(
            model_name='quote',
            name='down_votes',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quote',
            name='up_votes',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=True,
        ),
    ]
