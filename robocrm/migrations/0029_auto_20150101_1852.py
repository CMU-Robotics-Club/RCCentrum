# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import robocrm.fields


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0028_auto_20141226_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='dues_paid_year',
            field=models.BooleanField(help_text='Unchecked if only Semester membership was paid', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=robocrm.fields.CharNullField(help_text='9 Character Magnetic Card ID(found on Student ID)(Only you can see this ID)', max_length=9, unique=True, blank=True, null=True),
            preserve_default=True,
        ),
    ]
