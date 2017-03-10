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
                ('author', models.ForeignKey(to='users.Profile')),
                ('post', models.ForeignKey(related_name='comments', to='posts.Post')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
