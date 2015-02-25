# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='inventory',
            field=models.ForeignKey(to='Neverwherebot.Storage', blank=True),
            preserve_default=True,
        ),
    ]
