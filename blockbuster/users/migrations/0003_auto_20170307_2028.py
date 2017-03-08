# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170307_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='github',
            field=models.URLField(null=True),
        ),
    ]
