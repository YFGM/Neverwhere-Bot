# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0022_auto_20150305_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='craft',
            name='resources',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='part_time',
        ),
        migrations.AlterField(
            model_name='employee',
            name='job',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Job', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='worksite',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Worksite', null=True),
            preserve_default=True,
        ),
    ]
