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
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('is_public', models.BooleanField(default=True)),
                ('privacy', models.CharField(default=b'privacy_public', max_length=b'256', choices=[(b'private_to_one_friend', b'One Friend'), (b'private_to_me', b'Me'), (b'private_to_fof', b'Friends-of-Friends'), (b'privacy_public', b'Public'), (b'private_to_all_friends', b'Friends')])),
                ('content', models.CharField(max_length=500, null=True, blank=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('author', models.ForeignKey(related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('private_to', models.ForeignKey(related_name='received_private_posts', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
