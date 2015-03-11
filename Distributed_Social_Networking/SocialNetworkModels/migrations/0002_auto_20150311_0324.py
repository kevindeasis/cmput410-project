# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='friend_private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friends',
            name='own_private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friends',
            name='remote_private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='friends',
            name='sentrequest',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
