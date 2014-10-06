# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sponsors.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('name', models.CharField(max_length=30)),
                ('logo', models.ImageField(upload_to=sponsors.models.Sponsor.image_upload_to, null=True)),
                ('website', models.URLField(null=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
