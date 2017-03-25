# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_auto_20170325_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='host',
            field=models.URLField(unique=True, max_length=500),
        ),
    ]
