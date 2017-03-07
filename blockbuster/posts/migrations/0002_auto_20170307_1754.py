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
            name='author',
            field=models.ForeignKey(related_name='posts_created', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='private_to',
            field=models.ForeignKey(related_name='received_private_posts', to='users.UserProfile', null=True),
        ),
    ]
