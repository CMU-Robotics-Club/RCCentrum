# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import posters.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=30)),
                ('year', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=posters.models.Poster.image_upload_to)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
