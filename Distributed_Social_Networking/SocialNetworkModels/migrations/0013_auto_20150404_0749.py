# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0012_auto_20150404_0739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nodes',
            options={'verbose_name': 'Nodes', 'verbose_name_plural': 'Nodes'},
        ),
    ]
