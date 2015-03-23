# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0004_auto_20150322_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('post_id', models.CharField(max_length=200)),
                ('comment_id', django_extensions.db.fields.UUIDField(serialize=False, editable=False, primary_key=True, blank=True)),
                ('comment_text', models.CharField(max_length=200)),
                ('post_author', models.ForeignKey(to='SocialNetworkModels.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
