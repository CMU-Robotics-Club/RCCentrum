# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0003_auto_20140910_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='leaders',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
