# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_apirequest_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='apirequest',
            name='api_client',
            field=models.CharField(null=True, editable=False, max_length=50),
            preserve_default=True,
        ),
    ]
