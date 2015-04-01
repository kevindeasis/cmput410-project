# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0008_posts_publication_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_host',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='author_url',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='comment_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 15, 52, 4, 616408, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='content_content',
            field=models.CharField(default=datetime.datetime(2015, 3, 30, 15, 53, 1, 751761, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='content_source',
            field=models.CharField(default=datetime.datetime(2015, 3, 30, 15, 53, 16, 159466, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='content_type',
            field=models.CharField(default=datetime.datetime(2015, 3, 30, 15, 53, 24, 175477, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
