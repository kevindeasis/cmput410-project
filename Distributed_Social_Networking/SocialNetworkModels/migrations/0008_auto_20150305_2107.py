# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0007_auto_20150305_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
