# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0017_auto_20150303_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='employer_sent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='sent',
            field=models.DateField(default=datetime.datetime(2015, 3, 4, 13, 43, 33, 357000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='current_date',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='acre',
            name='crop',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Crop', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='acre',
            name='farm',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Worksite', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='acre',
            name='pesticide',
            field=models.ForeignKey(blank=True, to='Neverwherebot.ItemType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='acre',
            name='planted',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
