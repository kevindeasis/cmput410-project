# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0009_auto_20150308_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(upload_to=b'/static/profile_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(upload_to=b'/static/post_images/', blank=True),
            preserve_default=True,
        ),
    ]
