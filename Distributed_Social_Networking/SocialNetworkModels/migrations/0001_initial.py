# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_title', models.CharField(max_length=20)),
                ('post_text', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to=b'post_images', blank=True)),
                ('visibility', models.CharField(max_length=10, choices=[(b'PRIVATE', b'Private'), (b'PUBLIC', b'Public'), (b'FRIENDS', b'Friends'), (b'FRIENDSFRIENDS', b'Friend of a Friend')])),
                ('number_of_Likes', models.IntegerField(default=0)),
                ('post_author', models.ForeignKey(related_name='post_author', to='SocialNetworkModels.AuthorProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
