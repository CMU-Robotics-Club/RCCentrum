# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import officers.models


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0004_auto_20140912_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Officers',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('position', models.TextField(null=True)),
                ('image', models.ImageField(upload_to=officers.models.Officer.image_upload_to, null=True)),
                ('user', models.ForeignKey(to='robocrm.RoboUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
