# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0024_auto_20150306_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='rations',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
