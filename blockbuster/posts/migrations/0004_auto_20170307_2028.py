# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20170307_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='private_to',
            field=models.ForeignKey(related_name='received_private_posts', blank=True, to='users.UserProfile', null=True),
        ),
    ]
