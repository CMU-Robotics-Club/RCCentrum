# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import officers.models


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0004_auto_20140912_1719'),
        ('officers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('position', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=officers.models.Officer.image_upload_to, null=True)),
                ('description', models.TextField(null=True)),
                ('user', models.ForeignKey(to='robocrm.RoboUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='officers',
            name='user',
        ),
        migrations.DeleteModel(
            name='Officers',
        ),
    ]
