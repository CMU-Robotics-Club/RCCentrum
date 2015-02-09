# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import robocrm.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0036_auto_20150209_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=robocrm.fields.CharNullField(help_text='9 Character Magnetic Card ID(found on Student ID)(Only you can see this ID)', unique=True, blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Magnetic must be 9 numeric characters(0-9)', code='invalid_magnetic', regex='^[0-9]{9}$')], max_length=9),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=robocrm.fields.CharNullField(null=True, validators=[django.core.validators.RegexValidator(message='RFID must be 8 hexadecimal characters(0-9, A-F)', code='invalid_rfid', regex='^[A-F0-9]{8}$')], unique=True, blank=True, max_length=10),
            preserve_default=True,
        ),
    ]
