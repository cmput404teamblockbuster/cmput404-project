# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20170325_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.CharField(default=b'privacy_public', max_length=b'256', choices=[(b'privacy_public', b'Public'), (b'private_to_all_friends', b'Friends'), (b'private_to_one_friend', b'One Friend'), (b'private_to_me', b'Me'), (b'privacy_unlisted', b'Unlisted'), (b'privacy_server_only', b'Server Only'), (b'private_to_fof', b'Friends-of-Friends')]),
        ),
    ]
