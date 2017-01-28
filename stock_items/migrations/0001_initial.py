# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stock_items.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(choices=[('EB', 'eBench'), ('SH', 'Shop'), ('OT', 'Other')], max_length=2, default='EB')),
                ('quantity', models.PositiveIntegerField(null=True, blank=True)),
                ('reorder_url', models.URLField(null=True, max_length=255, blank=True)),
                ('datasheet', models.FileField(null=True, upload_to=stock_items.models.StockItem.datasheet_upload_to)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
