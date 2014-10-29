# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20141006_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='blurb',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, upload_to=projects.models.Project.image_upload_to, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='private_key',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='Length has to be 4', code='nomatch', regex='^.{4}$')], max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='website',
            field=models.URLField(null=True, blank=True),
        ),
    ]
