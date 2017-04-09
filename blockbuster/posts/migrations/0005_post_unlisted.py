# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20170409_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
    ]
