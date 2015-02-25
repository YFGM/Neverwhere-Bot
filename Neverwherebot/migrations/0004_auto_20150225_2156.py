# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0003_auto_20150225_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='house',
            field=models.ForeignKey(to='Neverwherebot.Building', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='character',
            name='inventory',
            field=models.ForeignKey(to='Neverwherebot.Storage', null=True),
            preserve_default=True,
        ),
    ]
