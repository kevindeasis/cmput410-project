# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0013_auto_20150404_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='foreign_id',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
