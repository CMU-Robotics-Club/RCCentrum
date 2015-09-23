# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import robocrm.models


class Migration(migrations.Migration):

    dependencies = [
        ('robocrm', '0052_robouser_tshirt_picked_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='robouser',
            name='resume',
            field=models.FileField(null=True, upload_to=robocrm.models.RoboUser.resume_upload_to),
        ),
    ]
