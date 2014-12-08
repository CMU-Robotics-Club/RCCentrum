# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20141128_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apirequest',
            name='meta',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
