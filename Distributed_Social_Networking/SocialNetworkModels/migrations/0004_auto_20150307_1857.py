# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0003_auto_20150307_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_id',
            field=models.IntegerField(unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
