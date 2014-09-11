# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='project',
        ),
        migrations.RemoveField(
            model_name='project',
            name='charge',
        ),
        migrations.RemoveField(
            model_name='project',
            name='primuser',
        ),
        migrations.RemoveField(
            model_name='project',
            name='users',
        ),
        migrations.AlterField(
            model_name='robouser',
            name='bench_status',
            field=models.CharField(max_length=2, default='GD', choices=[('GD', 'Good Standing'), ('FS', 'First Warning Recieved'), ('SD', 'Second Warning Recieved'), ('SB', 'Semester Ban'), ('CB', 'Club Ban')]),
        ),
        migrations.AlterField(
            model_name='robouser',
            name='shop_status',
            field=models.CharField(max_length=2, default='GD', choices=[('GD', 'Good Standing'), ('FS', 'First Warning Recieved'), ('SD', 'Second Warning Recieved'), ('SB', 'Semester Ban'), ('CB', 'Club Ban')]),
        ),
    ]
