# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0002_auto_20150311_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='mark_down',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
