# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0002_auto_20150225_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='inventory',
            field=models.ForeignKey(default=None, blank=True, to='Neverwherebot.Storage'),
            preserve_default=True,
        ),
    ]
