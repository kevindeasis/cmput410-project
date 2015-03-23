# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0005_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='post_author',
        ),
    ]
