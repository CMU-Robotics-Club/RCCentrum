# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tshirts.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TShirt',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('year', models.PositiveIntegerField()),
                ('front_image', models.ImageField(upload_to=tshirts.models.TShirt.front_image_upload_to)),
                ('back_image', models.ImageField(upload_to=tshirts.models.TShirt.back_image_upload_to)),
            ],
            options={
                'ordering': ['year', 'name'],
            },
            bases=(models.Model,),
        ),
    ]
