# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.CharField(default=b'PUBLIC', max_length=b'256', choices=[(b'PRIVATE', b'Me'), (b'PUBLIC', b'Public'), (b'FOF', b'Friends-of-Friends'), (b'privacy_unlisted', b'Unlisted'), (b'FRIENDS', b'Friends'), (b'SERVERONLY', b'Server Only')]),
        ),
    ]
