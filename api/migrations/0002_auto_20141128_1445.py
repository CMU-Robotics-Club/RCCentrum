# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apirequest',
            old_name='created_date',
            new_name='created_datetime',
        ),
        migrations.RenameField(
            model_name='apirequest',
            old_name='modified_date',
            new_name='updated_datetime',
        ),
    ]
