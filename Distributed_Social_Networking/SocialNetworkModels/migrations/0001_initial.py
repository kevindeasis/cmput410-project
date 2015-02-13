# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_username', models.CharField(max_length=200)),
                ('author_email', models.CharField(max_length=200)),
                ('author_password', models.CharField(max_length=200)),
                ('registration_date', models.DateTimeField(verbose_name=b'date registered')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_text', models.CharField(max_length=200)),
                ('number_of_Likes', models.IntegerField(default=0)),
                ('post_author', models.ForeignKey(to='SocialNetworkModels.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
