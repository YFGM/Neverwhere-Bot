# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0011_auto_20150228_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='unit',
        ),
        migrations.AddField(
            model_name='itemtype',
            name='unit',
            field=models.CharField(max_length=64, blank=True),
            preserve_default=True,
        ),
    ]
