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
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artist', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('song_url', models.URLField()),
                ('state', models.IntegerField(choices=[(0, b'proposed'), (1, b'rejected'), (2, b'arranging'), (3, b'current'), (4, b'retired')])),
                ('has_willing_arranger', models.BooleanField(default=False)),
                ('drive_link', models.URLField(null=True, blank=True)),
                ('arranger', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('suggested_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('arrange', 'Can arrange'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.IntegerField(choices=[(0, b'yes'), (1, b'no'), (2, b'meh')])),
                ('song', models.ForeignKey(to='songs.Song')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
