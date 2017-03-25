# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170320_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='host',
            field=models.CharField(default=b'http://127.0.0.1:8000/', max_length=100),
        ),
    ]
