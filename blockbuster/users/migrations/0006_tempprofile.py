# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=30)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('password', models.CharField(max_length=128)),
                ('is_accepted', models.BooleanField(default=False, help_text=b'Let this user join blockbuster?')),
            ],
        ),
    ]
