# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20141128_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apirequest',
            old_name='requester_id',
            new_name='updater_id',
        ),
        migrations.RenameField(
            model_name='apirequest',
            old_name='requester_type',
            new_name='updater_type',
        ),
    ]
