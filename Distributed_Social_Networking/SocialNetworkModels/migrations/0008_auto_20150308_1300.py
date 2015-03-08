# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SocialNetworkModels', '0007_auto_20150307_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initiator', models.ForeignKey(related_name='initiator', to=settings.AUTH_USER_MODEL)),
                ('reciever', models.ForeignKey(related_name='reciever', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Friends',
                'verbose_name_plural': 'Friends',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friends',
            unique_together=set([('initiator', 'reciever')]),
        ),
    ]
