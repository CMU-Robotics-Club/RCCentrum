# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import robocrm.fields
import robocrm.models
import django.core.validators
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0053_robouser_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=robocrm.fields.CharNullField(help_text='9 Character Magnetic Card ID (found on Student ID). Only you can see this ID.', null=True, blank=True, max_length=9, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_magnetic', message='Magnetic must be 9 numeric characters(0-9)', regex='^[0-9]{9}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='robouser',
            name='resume',
            field=models.FileField(upload_to=robocrm.models.RoboUser.resume_upload_to, help_text='Upload your resume to be included in the Roboclub resume book (pdf format only)', null=True, blank=True, storage=django.core.files.storage.FileSystemStorage(location='/home/aaron/roboclub/roboticsclub.org/private', base_url='/private/')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='robouser',
            name='rfid',
            field=robocrm.fields.CharNullField(help_text='8 Hex-digit RFID. Some card readers return decimal number in opposite endianness.', null=True, blank=True, max_length=10, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_rfid', message='RFID must be 8 hexadecimal characters(0-9, A-F)', regex='^[A-F0-9]{8}$')]),
            preserve_default=True,
        ),
    ]
