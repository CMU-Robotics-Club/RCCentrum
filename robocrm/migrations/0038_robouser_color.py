# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0037_auto_20150209_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='robouser',
            name='color',
            field=models.CharField(max_length=6, help_text='Color that can be used by Projects', validators=[django.core.validators.RegexValidator(code='invalid_color', regex='^[0-9][A-F]{6}$', message='Must be a valid color code(6 hexadecimal characters)(ex. "FF0000" is red)')], default='FF0000'),
            preserve_default=True,
        ),
    ]
