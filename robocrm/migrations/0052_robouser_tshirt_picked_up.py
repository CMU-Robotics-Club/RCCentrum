# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0051_auto_20150405_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='robouser',
            name='tshirt_picked_up',
            field=models.BooleanField(help_text='Checked if student received a tshirt', default=False),
        ),
    ]
