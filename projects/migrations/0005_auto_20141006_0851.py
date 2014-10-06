# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_private_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='private_key',
            field=models.CharField(max_length=50),
        ),
    ]
