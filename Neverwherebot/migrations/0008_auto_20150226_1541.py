# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0007_auto_20150225_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='bl',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='character',
            name='re',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
