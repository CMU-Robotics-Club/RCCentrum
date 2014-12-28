# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20141208_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apirequest',
            name='endpoint',
            field=models.CharField(max_length=30, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apirequest',
            name='user',
            field=models.ForeignKey(null=True, to='robocrm.RoboUser', editable=False),
            preserve_default=True,
        ),
    ]
