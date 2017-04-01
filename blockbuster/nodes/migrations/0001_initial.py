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
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.URLField(unique=True, max_length=500)),
                ('is_allowed', models.BooleanField(default=True)),
                ('username_for_node', models.CharField(max_length=60, null=True, blank=True)),
                ('password_for_node', models.CharField(max_length=60, null=True, blank=True)),
                ('api_endpoint', models.CharField(help_text=b'the root for their api access.', max_length=30, blank=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
