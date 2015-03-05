# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0008_auto_20150305_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='date_posted',
        ),
    ]
