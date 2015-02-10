# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0040_auto_20150210_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='color',
            field=models.CharField(max_length=60, validators=[django.core.validators.RegexValidator(code='invalid_color', message='Must be a valid color code(multiple of 6 hexadecimal characters)(ex. "FF0000" is red, FF000000FF00 red-green pattern)', regex='(?:[0-9A-F]{6})*')], help_text='Color (pattern, up to 10 colors,) that can be used by Projects(up to 60 hexadecimal characters)', default='FF0000'),
            preserve_default=True,
        ),
    ]
