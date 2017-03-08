# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20170307_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
