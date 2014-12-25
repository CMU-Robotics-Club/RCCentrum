# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotetron', '0005_auto_20141225_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='down_votes',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quote',
            name='up_votes',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=True,
        ),
    ]
