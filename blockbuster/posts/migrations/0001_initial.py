# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('source', models.URLField(help_text=b'Where the post was last from', max_length=100, null=True, blank=True)),
                ('origin', models.URLField(help_text=b'Where the post originated', max_length=100, null=True, blank=True)),
                ('description', models.CharField(max_length=150, null=True, blank=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('privacy', models.CharField(default=b'privacy_public', max_length=b'256', choices=[(b'privacy_public', b'Public'), (b'private_to_all_friends', b'Friends'), (b'private_to_one_friend', b'One Friend'), (b'private_to_me', b'Me'), (b'privacy_unlisted', b'Unlisted'), (b'privacy_server_only', b'Server Only'), (b'private_to_fof', b'Friends-of-Friends')])),
                ('content', models.CharField(max_length=1000000, null=True, blank=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('contentType', models.CharField(default=b'text/plain', max_length=50, choices=[(b'text/markdown', b'text/markdown'), (b'text/plain', b'text/plain'), (b'application/base64', b'application/base64'), (b'image/png;base64', b'image/png;base64'), (b'image/jpeg;base64', b'image/jpeg;base64')])),
                ('author', models.ForeignKey(related_name='posts', to='users.Profile')),
                ('private_to', models.ForeignKey(related_name='received_private_posts', blank=True, to='users.Profile', null=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
