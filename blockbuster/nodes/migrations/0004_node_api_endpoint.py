# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0003_auto_20170325_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='api_endpoint',
            field=models.CharField(help_text=b'the root for their api access.', max_length=30, blank=True),
        ),
    ]
