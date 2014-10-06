# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_last_api_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='private_key',
            field=models.CharField(max_length=50, default='32Fdd53EaFb5864ea9DF'),
            preserve_default=True,
        ),
    ]
