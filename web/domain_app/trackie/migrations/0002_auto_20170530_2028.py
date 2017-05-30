# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 18:28
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trackie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('display_name', models.CharField(max_length=255, unique=True, verbose_name='Display name')),
                ('type', models.CharField(choices=[('BigIntegerField', 'BigIntegerField'), ('BooleanField', 'BooleanField'), ('DateField', 'DateField'), ('DateTimeField', 'DateTimeField'), ('DurationField', 'DurationField'), ('FloatField', 'FloatField'), ('IntegerField', 'IntegerField'), ('PositiveIntegerField', 'PositiveIntegerField'), ('PositiveSmallIntegerField', 'PositiveSmallIntegerField'), ('SmallIntegerField', 'SmallIntegerField'), ('TextField', 'TextField'), ('TimeField', 'TimeField'), ('URLField', 'URLField')], help_text="Django's field type", max_length=255, verbose_name='Type')),
            ],
            options={
                'verbose_name_plural': 'Race Field types',
                'verbose_name': 'Race field type',
            },
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Projections',
                'verbose_name': 'Projection',
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the race', max_length=255, verbose_name='Name')),
                ('start', models.DateTimeField(verbose_name='Begins at')),
                ('real_start', models.DateTimeField(blank=True, null=True, verbose_name='First data received at')),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('real_end', models.DateTimeField(blank=True, null=True, verbose_name='Last data received at')),
                ('estimated_duration', models.DurationField(help_text='[DD] [HH:[MM:]]ss', verbose_name='Estimated duration')),
            ],
            options={
                'verbose_name_plural': 'Races',
                'verbose_name': 'Race',
            },
        ),
        migrations.CreateModel(
            name='RaceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received', models.DateTimeField()),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('race', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data', to='trackie.Race')),
            ],
        ),
        migrations.CreateModel(
            name='Racer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('full_name', models.CharField(blank=True, help_text='Only for search purpose (automatically filled)', max_length=255, null=True, verbose_name='Full name')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('death_date', models.DateField(blank=True, null=True, verbose_name='Date of death')),
                ('about', models.TextField(blank=True, null=True, verbose_name='About racer')),
                ('photo', versatileimagefield.fields.VersatileImageField(blank=True, help_text='Image will be resized and cropped to 175x200, Maximum image size is 512 KiB', null=True, upload_to='racers/', verbose_name="Racer's photo")),
            ],
            options={
                'verbose_name_plural': 'Racers',
                'verbose_name': 'Racer',
            },
        ),
        migrations.CreateModel(
            name='RacerInRace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='racers', to='trackie.Race')),
                ('racer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='races', to='trackie.Racer')),
            ],
        ),
        migrations.CreateModel(
            name='RaceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Type of the race', max_length=255, verbose_name='Race type')),
                ('public', models.BooleanField(default=False, help_text='Will be available for others?', verbose_name='Public')),
                ('fields', models.ManyToManyField(blank=True, help_text='All field will be required', related_name='races', to='trackie.FieldType')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='race_types', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name_plural': 'Race types',
                'verbose_name': 'Race type',
            },
        ),
        migrations.CreateModel(
            name='SportType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the sport', max_length=255, unique=True, verbose_name='Sport name')),
                ('slug', models.SlugField(help_text='Name for the API', max_length=255, unique=True, verbose_name='Slug')),
                ('icon', models.ImageField(blank=True, help_text='Choose icon', null=True, upload_to='static/images/sport/', verbose_name='Icon')),
            ],
            options={
                'verbose_name_plural': 'Sport types',
                'verbose_name': 'Sport type',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the Tournament', max_length=255, verbose_name='Name')),
                ('owner', models.ForeignKey(help_text='Administrator of the Tournament', on_delete=django.db.models.deletion.CASCADE, related_name='tournaments', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('sport', models.ForeignKey(help_text='Type of the sport of the tournament', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournaments', to='trackie.SportType', verbose_name='Sport')),
            ],
            options={
                'verbose_name_plural': 'Tournaments',
                'verbose_name': 'Tournament',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Track name')),
                ('file', models.FileField(help_text="The file can't be changed. Maximum file size is 512 KiB", upload_to='maps/')),
                ('public', models.BooleanField(default=False, verbose_name='Public')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tracks', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name_plural': 'Tracks',
                'verbose_name': 'Track',
            },
        ),
        migrations.AddField(
            model_name='racedata',
            name='racer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trackie.RacerInRace'),
        ),
        migrations.AddField(
            model_name='race',
            name='participants',
            field=models.ManyToManyField(through='trackie.RacerInRace', to='trackie.Racer'),
        ),
        migrations.AddField(
            model_name='race',
            name='projection',
            field=models.ForeignKey(blank=True, help_text='Default is EPSG:3857', null=True, on_delete=django.db.models.deletion.SET_NULL, to='trackie.Projection', verbose_name='Projection'),
        ),
        migrations.AddField(
            model_name='race',
            name='tournament',
            field=models.ForeignKey(help_text='Select under which tournament is assigned', on_delete=django.db.models.deletion.CASCADE, related_name='races', to='trackie.Tournament', verbose_name='Tournament'),
        ),
        migrations.AddField(
            model_name='race',
            name='track',
            field=models.ForeignKey(help_text='Select track map', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='races', to='trackie.Track', verbose_name='Track'),
        ),
        migrations.AddField(
            model_name='race',
            name='type',
            field=models.ForeignKey(help_text='Determine race type', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='races', to='trackie.RaceType', verbose_name='Type'),
        ),
        migrations.AlterUniqueTogether(
            name='racerinrace',
            unique_together=set([('race', 'number', 'racer')]),
        ),
    ]