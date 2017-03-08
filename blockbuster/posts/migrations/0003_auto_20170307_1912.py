# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170307_1754'),
        ('posts', '0002_auto_20170307_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='posts', to='users.UserProfile'),
        ),
    ]
