# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories', 'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='qa',
            options={'verbose_name_plural': 'QAs', 'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='qa',
            name='order',
            field=models.IntegerField(),
        ),
    ]
