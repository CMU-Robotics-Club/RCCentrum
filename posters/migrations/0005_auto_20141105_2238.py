# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posters', '0004_auto_20141105_2003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poster',
            options={'ordering': ['year', 'name']},
        ),
        migrations.RemoveField(
            model_name='poster',
            name='order',
        ),
    ]
