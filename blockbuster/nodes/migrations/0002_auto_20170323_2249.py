# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='url',
            new_name='host',
        ),
        migrations.RemoveField(
            model_name='node',
            name='permission',
        ),
        migrations.AddField(
            model_name='node',
            name='is_allowed',
            field=models.BooleanField(default=True),
        ),
    ]
