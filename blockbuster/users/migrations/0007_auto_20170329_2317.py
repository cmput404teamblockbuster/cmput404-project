# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_tempprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TempProfile',
            new_name='NewUser',
        ),
    ]
