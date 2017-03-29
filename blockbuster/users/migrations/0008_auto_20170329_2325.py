# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20170329_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newuser',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='newuser',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 29, 23, 25, 13, 632968, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
