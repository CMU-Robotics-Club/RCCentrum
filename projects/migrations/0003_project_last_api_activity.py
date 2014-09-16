# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='last_api_activity',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
