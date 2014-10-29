# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20141029_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='blurb',
            field=models.TextField(null=True, help_text='Miniature description displayed on project overview page.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(null=True, help_text='Full description displayed on project detail page.', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, default='logo.png', upload_to=projects.models.Project.image_upload_to),
        ),
        migrations.AlterField(
            model_name='project',
            name='private_key',
            field=models.CharField(max_length=50),
        ),
    ]
