# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0010_auto_20150404_0728'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nodes',
            options={'verbose_name': 'Node'},
        ),
        migrations.AlterModelTable(
            name='nodes',
            table='Nodes',
        ),
    ]
