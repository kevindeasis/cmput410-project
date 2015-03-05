# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0006_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 5, 21, 4, 18, 573300, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='post_reciever',
            field=models.ForeignKey(related_name='post_reciever', default=datetime.datetime(2015, 3, 5, 21, 4, 37, 541280, tzinfo=utc), to='SocialNetworkModels.AuthorProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_author',
            field=models.ForeignKey(related_name='post_author', to='SocialNetworkModels.AuthorProfile'),
            preserve_default=True,
        ),
    ]
