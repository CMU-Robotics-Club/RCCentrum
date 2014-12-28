# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20141227_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='apirequest',
            name='success',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
