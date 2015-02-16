# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20141029_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='private_key',
            field=models.CharField(max_length=50, default=projects.models.create_private_key),
            preserve_default=True,
        ),
    ]
