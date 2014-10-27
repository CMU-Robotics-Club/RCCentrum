# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0019_auto_20141021_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robouser',
            name='sec_major_one',
        ),
        migrations.RemoveField(
            model_name='robouser',
            name='sec_major_two',
        ),
        migrations.AlterField(
            model_name='robouser',
            name='cell',
            field=models.DecimalField(help_text='Cell Phone # if you wish to provide it to Officers', blank=True, decimal_places=0, null=True, max_digits=10),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='magnetic',
            field=models.CharField(help_text='9 Character Magnetic Card ID(found on Student ID)', max_length=9, null=True, blank=True),
        ),
    ]
