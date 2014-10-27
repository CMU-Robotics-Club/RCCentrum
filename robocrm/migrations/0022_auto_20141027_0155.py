# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import robocrm.fields


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0021_auto_20141027_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=robocrm.fields.CharNullField(null=True, blank=True, unique=True, max_length=9, help_text='9 Character Magnetic Card ID(found on Student ID)'),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=robocrm.fields.CharNullField(null=True, blank=True, unique=True, max_length=10),
        ),
    ]
