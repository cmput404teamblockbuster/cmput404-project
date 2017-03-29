# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170329_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='created',
            field=models.DateTimeField(editable=False),
        ),
    ]
