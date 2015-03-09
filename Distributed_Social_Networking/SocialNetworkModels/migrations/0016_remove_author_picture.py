# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0015_auto_20150309_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='picture',
        ),
    ]
