# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetworkModels', '0005_auto_20150305_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_text', models.CharField(max_length=200)),
                ('number_of_Likes', models.IntegerField(default=0)),
                ('post_author', models.ForeignKey(to='SocialNetworkModels.AuthorProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
