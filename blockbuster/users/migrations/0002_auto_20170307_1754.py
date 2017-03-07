# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170307_1754'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0002_auto_20170307_1754'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('github', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userrelationship',
            name='initiator',
            field=models.ForeignKey(related_name='initiated_relationships', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userrelationship',
            name='receiver',
            field=models.ForeignKey(related_name='received_relationships', to='users.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='userrelationship',
            unique_together=set([('initiator', 'receiver')]),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
