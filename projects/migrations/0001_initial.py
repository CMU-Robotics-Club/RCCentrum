# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0004_auto_20140912_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to=projects.models.Project.image_upload_to, null=True)),
                ('blurb', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('website', models.URLField(null=True)),
                ('leaders', models.ManyToManyField(related_name='u+', to='robocrm.RoboUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
