# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0006_auto_20150307_2004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='username',
            new_name='user',
        ),
    ]
