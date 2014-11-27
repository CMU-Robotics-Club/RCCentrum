# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('robocrm', '0023_auto_20141120_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('endpoint', models.CharField(max_length=30)),
                ('requester_id', models.PositiveIntegerField()),
                ('meta', models.CharField(blank=True, max_length=50, null=True)),
                ('requester_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to='robocrm.RoboUser', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
