# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0004_auto_20140912_1719'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='robouser',
            options={'ordering': ['user__username']},
        ),
    ]
