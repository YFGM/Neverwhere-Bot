# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0021_auto_20150305_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='craft',
            name='value',
        ),
        migrations.RemoveField(
            model_name='craft',
            name='wr',
        ),
        migrations.AddField(
            model_name='itemtype',
            name='wr',
            field=models.FloatField(default=0.5),
            preserve_default=False,
        ),
    ]
