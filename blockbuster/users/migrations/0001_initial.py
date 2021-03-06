# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(editable=False)),
                ('username', models.CharField(unique=True, max_length=30)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('password', models.CharField(max_length=128)),
                ('is_accepted', models.BooleanField(default=False, help_text=b'Let this user join blockbuster?')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(default=None, max_length=30, editable=False)),
                ('github', models.URLField(null=True, blank=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('host', models.CharField(default='example.com', max_length=100)),
                ('bio', models.CharField(max_length=150, null=True, blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'status_friendship_pending', max_length=b'100', choices=[(b'status_following', b'Following'), (b'status_friendship_pending', b'Pending'), (b'status_friends', b'Friends')])),
                ('initiator', models.ForeignKey(related_name='initiated_relationships', to='users.Profile')),
                ('receiver', models.ForeignKey(related_name='received_relationships', to='users.Profile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userrelationship',
            unique_together=set([('initiator', 'receiver')]),
        ),
    ]
