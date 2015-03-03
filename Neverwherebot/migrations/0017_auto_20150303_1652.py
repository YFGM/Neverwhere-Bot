# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0016_auto_20150303_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpgradeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('unique', models.BooleanField(default=False)),
                ('slug', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=512)),
                ('required_item', models.ForeignKey(to='Neverwherebot.ItemType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='upgrade',
            name='name',
        ),
        migrations.AddField(
            model_name='job',
            name='worksite',
            field=models.ForeignKey(default=0, to='Neverwherebot.Worksite'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='upgrade',
            name='type',
            field=models.ForeignKey(default='', to='Neverwherebot.UpgradeType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job',
            name='default_salary',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='process',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Process', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upgrade',
            name='acre',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Acre', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upgrade',
            name='building',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Building', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upgrade',
            name='storage',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Storage', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upgrade',
            name='tunnel',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Tunnel', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='upgrade',
            name='worksite',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Worksite', null=True),
            preserve_default=True,
        ),
    ]
