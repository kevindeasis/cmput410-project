# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0008_auto_20150308_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='id',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='photo',
        ),
        migrations.AddField(
            model_name='author',
            name='picture',
            field=models.ImageField(upload_to=b'profile_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_id',
            field=django_extensions.db.fields.UUIDField(primary_key=True, default=1, serialize=False, editable=False, blank=True),
            preserve_default=False,
        ),
    ]
