# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialmedia',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='socialmedia',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=1),
            preserve_default=False,
        ),
    ]
