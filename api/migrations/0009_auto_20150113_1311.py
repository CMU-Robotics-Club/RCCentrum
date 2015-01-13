# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_apirequest_api_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apirequest',
            name='updater_id',
            field=models.PositiveIntegerField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apirequest',
            name='updater_type',
            field=models.ForeignKey(to='contenttypes.ContentType', editable=False),
            preserve_default=True,
        ),
    ]
