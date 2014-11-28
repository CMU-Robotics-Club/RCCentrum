# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('officers', '0005_officer_memo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='memo',
            field=models.TextField(null=True),
        ),
    ]
