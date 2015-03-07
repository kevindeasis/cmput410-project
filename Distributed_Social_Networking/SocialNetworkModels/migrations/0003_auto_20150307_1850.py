# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0002_auto_20150307_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='post_id',
            field=models.IntegerField(unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_author',
            field=models.ForeignKey(to='SocialNetworkModels.Author'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posts',
            name='visibility',
            field=models.CharField(default=b'PUBLIC', max_length=10, choices=[(b'PRIVATE', b'Private'), (b'PUBLIC', b'Public'), (b'FRIENDS', b'Friends'), (b'FRIENDSFRIENDS', b'Friend of a Friend')]),
            preserve_default=True,
        ),
    ]
