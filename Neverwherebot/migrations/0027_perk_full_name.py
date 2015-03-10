# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0026_character_foodstore'),
    ]

    operations = [
        migrations.AddField(
            model_name='perk',
            name='full_name',
            field=models.CharField(default='Fix me', unique=False, max_length=128),
            preserve_default=False,
        ),
    ]
