# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0002_auto_20140910_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='blurb',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(upload_to=projects.models.Project.image_upload_to, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='leaders',
            field=models.ManyToManyField(to='robocrm.RoboUser', related_name='u+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='website',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
