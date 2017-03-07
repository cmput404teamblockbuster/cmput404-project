# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('github', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'status_friendship_pending', max_length=b'100', verbose_name=[(b'status_following', b'Following'), (b'status_friendship_pending', b'Pending'), (b'status_friends', b'Friends')])),
                ('initiator', models.ForeignKey(related_name='initiated_relationships', to='users.User')),
                ('receiver', models.ForeignKey(related_name='received_relationships', to='users.User')),
            ],
        ),
    ]
