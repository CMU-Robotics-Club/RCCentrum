# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0033_remove_machine_maint'),
    ]

    operations = [
        migrations.AddField(
            model_name='robouser',
            name='rfid_card',
            field=models.CharField(default='CMU', max_length=5, choices=[('CMU', 'CMU ID'), ('PIT', 'PIT ID'), ('OTHER', 'OTHER ID')]),
            preserve_default=True,
        ),
    ]
