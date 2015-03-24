# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0006_remove_comments_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_author',
            field=models.CharField(default='aaa', max_length=200),
            preserve_default=False,
        ),
    ]
