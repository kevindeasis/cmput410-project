# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0008_auto_20150308_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
