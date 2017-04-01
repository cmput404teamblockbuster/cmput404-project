# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('body', models.CharField(max_length=500)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('contentType', models.CharField(default=b'text/plain', max_length=50, choices=[(b'text/markdown', b'text/markdown'), (b'text/plain', b'text/plain'), (b'application/base64', b'application/base64'), (b'image/png;base64', b'image/png;base64'), (b'image/jpeg;base64', b'image/jpeg;base64')])),
                ('author', models.ForeignKey(to='users.Profile')),
                ('post', models.ForeignKey(related_name='comments', to='posts.Post')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
