# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(default=None, max_length=30, editable=False),
        ),
        migrations.AlterField(
            model_name='userrelationship',
            name='status',
            field=models.CharField(default=b'status_friendship_pending', max_length=b'100', choices=[(b'status_following', b'Following'), (b'status_friendship_pending', b'Pending'), (b'status_friends', b'Friends')]),
        ),
    ]
