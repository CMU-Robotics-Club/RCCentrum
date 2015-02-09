# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import robocrm.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0035_auto_20150130_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=robocrm.fields.CharNullField(null=True, unique=True, max_length=10, blank=True, validators=[django.core.validators.RegexValidator(code='invalid_rfid', message='RFID must be 8 hexa-decimal characters(0-9, A-F)', regex='^[A-F0-9]{8}$')]),
            preserve_default=True,
        ),
    ]
