# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=30)),
                ('tstart', models.DateTimeField()),
                ('tend', models.DateTimeField()),
                ('succ', models.BooleanField(default=False)),
                ('imgurl', models.URLField()),
                ('matuse', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('type', models.CharField(max_length=20)),
                ('id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('maint', models.BooleanField(default=False)),
                ('dstart', models.DateTimeField(null=True, blank=True)),
                ('dend', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('charge', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoboResource',
            fields=[
                ('type', models.CharField(max_length=30)),
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('checked_out', models.BooleanField(default=False)),
                ('time_out', models.DateTimeField(null=True, blank=True)),
                ('time_due', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoboUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rfid', models.CharField(max_length=10, null=True, blank=True)),
                ('cell', models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)),
                ('class_level', models.CharField(default='UG', max_length=2, choices=[('UG', 'Undergraduate'), ('GR', 'Graduate Student'), ('AF', 'Non-Student CMU Affiliate'), ('OH', 'Other User')])),
                ('grad_year', models.IntegerField(null=True, blank=True)),
                ('major', models.CharField(max_length=20)),
                ('sec_major_one', models.CharField(max_length=20, null=True, blank=True)),
                ('sec_major_two', models.CharField(max_length=20, null=True, blank=True)),
                ('club_rank', models.CharField(default='JM', max_length=2, choices=[('JM', 'Junior Member'), ('SM', 'Senior Member'), ('OM', 'Officer')])),
                ('dues_paid', models.DateField(null=True, blank=True)),
                ('tshirt_rec', models.BooleanField(default=False)),
                ('bench_status', models.CharField(default='GD', max_length=2, choices=[('GD', 'Good Standing'), ('FS', 'First Warning Recieved'), ('SD', 'Second Warning Recieved'), ('S', 'Semester Ban'), ('C', 'Club Ban')])),
                ('shop_status', models.CharField(default='GD', max_length=2, choices=[('GD', 'Good Standing'), ('FS', 'First Warning Recieved'), ('SD', 'Second Warning Recieved'), ('S', 'Semester Ban'), ('C', 'Club Ban')])),
                ('machines', models.ManyToManyField(to='robocrm.Machine', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='roboresource',
            name='officer',
            field=models.ForeignKey(related_name='o+', blank=True, to='robocrm.RoboUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='roboresource',
            name='user',
            field=models.ForeignKey(related_name='u+', blank=True, to='robocrm.RoboUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='primuser',
            field=models.ForeignKey(related_name='pri+', to='robocrm.RoboUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='u+', to='robocrm.RoboUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='machine',
            field=models.ForeignKey(to='robocrm.Machine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(to='robocrm.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(to='robocrm.RoboUser', null=True),
            preserve_default=True,
        ),
    ]
