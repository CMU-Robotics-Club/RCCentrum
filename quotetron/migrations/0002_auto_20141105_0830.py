# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotetron', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='quote',
            field=models.TextField(),
        ),
    ]
