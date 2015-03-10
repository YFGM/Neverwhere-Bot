# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0028_auto_20150310_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perk',
            name='full_name',
            field=models.CharField(unique=True, max_length=128),
            preserve_default=True,
        ),
    ]
