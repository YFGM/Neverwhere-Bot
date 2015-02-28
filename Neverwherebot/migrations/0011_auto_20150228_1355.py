# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0010_player_current_character'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='amount',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
    ]
