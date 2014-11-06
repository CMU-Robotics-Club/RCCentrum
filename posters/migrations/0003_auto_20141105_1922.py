# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posters', '0002_auto_20141105_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
