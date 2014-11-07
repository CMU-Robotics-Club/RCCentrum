# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields
import posters.models


class Migration(migrations.Migration):

    dependencies = [
        ('posters', '0005_auto_20141105_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=posters.models.Poster.image_upload_to),
        ),
    ]
