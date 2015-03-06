# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0023_auto_20150305_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity', models.CharField(max_length=64, null=True, blank=True)),
                ('day', models.IntegerField(null=True, blank=True)),
                ('hour', models.IntegerField(null=True, blank=True)),
                ('on_idle', models.BooleanField(default=False)),
                ('persistant', models.BooleanField(default=False)),
                ('acre', models.ForeignKey(blank=True, to='Neverwherebot.Acre', null=True)),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
                ('craft', models.ForeignKey(blank=True, to='Neverwherebot.Craft', null=True)),
                ('employment', models.ForeignKey(blank=True, to='Neverwherebot.Employee', null=True)),
                ('process', models.ForeignKey(blank=True, to='Neverwherebot.Process', null=True)),
                ('tunnel', models.ForeignKey(blank=True, to='Neverwherebot.Tunnel', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='ac',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='ap',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='bonus',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='damage',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='re',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='spoils',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='weapon_class',
        ),
        migrations.RemoveField(
            model_name='itemtype',
            name='wearable',
        ),
        migrations.RemoveField(
            model_name='job',
            name='process',
        ),
        migrations.AddField(
            model_name='employee',
            name='process',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Process', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemtype',
            name='slot',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
