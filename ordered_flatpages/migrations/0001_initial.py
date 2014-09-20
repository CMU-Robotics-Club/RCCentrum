# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedFlatPage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='flatpages.FlatPage')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'abstract': False,
                'ordering': ('order',),
            },
            bases=('flatpages.flatpage', models.Model),
        ),
    ]
