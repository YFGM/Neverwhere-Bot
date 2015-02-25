# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0006_auto_20150225_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='bl',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='character',
            name='re',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
