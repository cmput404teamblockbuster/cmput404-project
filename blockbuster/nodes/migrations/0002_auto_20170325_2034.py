# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='password_for_node',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='node',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='node',
            name='username_for_node',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
    ]
