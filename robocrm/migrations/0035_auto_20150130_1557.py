# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0034_robouser_rfid_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robouser',
            name='rfid_card',
            field=models.CharField(default='CMU', choices=[('CMU', 'CMU ID'), ('PITT', 'PITT ID'), ('OTHER', 'OTHER ID')], max_length=5),
            preserve_default=True,
        ),
    ]
