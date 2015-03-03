# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0015_auto_20150228_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='value',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
