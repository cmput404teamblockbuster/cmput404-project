# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('github', models.URLField(null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'status_friendship_pending', max_length=b'100', verbose_name=[(b'status_following', b'Following'), (b'status_friendship_pending', b'Pending'), (b'status_friends', b'Friends')])),
                ('initiator', models.ForeignKey(related_name='initiated_relationships', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(related_name='received_relationships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userrelationship',
            unique_together=set([('initiator', 'receiver')]),
        ),
    ]
