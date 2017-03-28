# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20170326_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.URLField(max_length=150, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='origin',
            field=models.URLField(help_text=b'Where the post originated', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.URLField(help_text=b'Where the post was last from', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
