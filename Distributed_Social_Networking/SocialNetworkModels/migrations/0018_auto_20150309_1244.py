# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SocialNetworkModels', '0017_author_picture'),
    ]

    operations = [
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
        migrations.AlterUniqueTogether(
            name='follows',
            unique_together=set([('followed', 'follower')]),
        ),
        migrations.AddField(
            model_name='friends',
            name='approvedrequest',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friends',
            name='fof_private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friends',
            name='sentrequest',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
