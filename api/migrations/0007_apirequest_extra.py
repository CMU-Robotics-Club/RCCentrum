# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_apirequest_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='apirequest',
            name='extra',
            field=models.TextField(editable=False, null=True),
            preserve_default=True,
        ),
    ]
