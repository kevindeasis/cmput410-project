# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0009_auto_20150330_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nodes',
            fields=[
                ('node_id', models.AutoField(serialize=False, primary_key=True)),
                ('host_url', models.CharField(unique=True, max_length=200)),
                ('host_name', models.CharField(max_length=200)),
                ('host_password', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='posts',
            name='content_content',
        ),
    ]
