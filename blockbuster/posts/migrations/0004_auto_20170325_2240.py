# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20170321_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='contentType',
            field=models.CharField(default=b'text/plain', max_length=50, choices=[(b'text/markdown', b'text/markdown'), (b'text/plain', b'text/plain'), (b'application/base64', b'application/base64'), (b'image/png;base64', b'image/png;base64'), (b'image/jpeg;base64', b'image/jpeg;base64')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
