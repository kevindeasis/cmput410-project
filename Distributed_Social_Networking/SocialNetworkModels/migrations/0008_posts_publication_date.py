# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0007_comments_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 25, 22, 18, 38, 308504, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
