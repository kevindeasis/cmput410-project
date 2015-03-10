# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('github_username', models.CharField(max_length=128, blank=True)),
                ('picture', models.ImageField(upload_to=b'static/profile_images/', blank=True)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hide', models.BooleanField(default=False)),
                ('followed', models.ForeignKey(related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Following',
                'verbose_name_plural': 'Followers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentrequest', models.BooleanField(default=True)),
                ('approvedrequest', models.BooleanField(default=False)),
                ('fof_private', models.BooleanField(default=False)),
                ('initiator', models.ForeignKey(related_name='initiator', to=settings.AUTH_USER_MODEL)),
                ('reciever', models.ForeignKey(related_name='reciever', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Friends',
                'verbose_name_plural': 'Friends',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', django_extensions.db.fields.UUIDField(serialize=False, editable=False, primary_key=True, blank=True)),
                ('post_title', models.CharField(max_length=20)),
                ('post_text', models.CharField(max_length=200)),
                ('visibility', models.CharField(default=b'PUBLIC', max_length=10, choices=[(b'PRIVATE', b'Private'), (b'PUBLIC', b'Public'), (b'FRIENDS', b'Friends'), (b'FOAF', b'Friend of a Friend')])),
                ('image', models.ImageField(upload_to=b'static/post_images/', blank=True)),
                ('post_author', models.ForeignKey(to='SocialNetworkModels.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friends',
            unique_together=set([('initiator', 'reciever')]),
        ),
        migrations.AlterUniqueTogether(
            name='follows',
            unique_together=set([('followed', 'follower')]),
        ),
    ]
