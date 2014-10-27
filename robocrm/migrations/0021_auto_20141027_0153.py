# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import robocrm.fields


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0020_auto_20141027_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=robocrm.fields.CharNullField(max_length=9, null=True, help_text='9 Character Magnetic Card ID(found on Student ID)', blank=True),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=robocrm.fields.CharNullField(max_length=10, null=True, blank=True),
        ),
    ]
