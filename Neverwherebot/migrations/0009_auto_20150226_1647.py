# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0008_auto_20150226_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='prey',
            name='name',
            field=models.CharField(default=b'Thingy', unique=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='skill',
            name='slug',
            field=models.CharField(default=b'FIX ME', unique=True, max_length=128),
            preserve_default=True,
        ),
    ]
