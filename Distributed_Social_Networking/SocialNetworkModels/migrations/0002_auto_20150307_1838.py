# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('SocialNetworkModels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('github_username', models.CharField(max_length=128, blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='authorprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='number_of_Likes',
        ),
        migrations.AddField(
            model_name='posts',
            name='image',
            field=models.ImageField(upload_to=b'post_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_author',
            field=models.ForeignKey(related_name='post_author', to='SocialNetworkModels.Author'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='AuthorProfile',
        ),
    ]
