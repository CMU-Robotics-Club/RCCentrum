# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0008_auto_20141128_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='description',
            field=models.TextField(blank=True, help_text='Description about what this channel is used for', null=True),
            preserve_default=True,
        ),
    ]
