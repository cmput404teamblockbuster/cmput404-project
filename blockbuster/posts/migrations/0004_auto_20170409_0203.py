# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20170409_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.CharField(default=b'PUBLIC', max_length=b'256', choices=[(b'FOAF', b'Friends-of-Friends'), (b'PRIVATE', b'Private'), (b'PUBLIC', b'Public'), (b'privacy_unlisted', b'Unlisted'), (b'FRIENDS', b'Friends'), (b'SERVERONLY', b'Server Only')]),
        ),
    ]
