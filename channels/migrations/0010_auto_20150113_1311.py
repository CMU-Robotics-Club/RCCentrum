# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0009_channel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='updater_id',
            field=models.PositiveIntegerField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='channel',
            name='updater_type',
            field=models.ForeignKey(to='contenttypes.ContentType', editable=False),
            preserve_default=True,
        ),
    ]
