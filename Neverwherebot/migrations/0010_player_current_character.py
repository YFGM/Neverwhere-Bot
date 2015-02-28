# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0009_auto_20150226_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='current_character',
            field=models.ForeignKey(related_name='p', to='Neverwherebot.Character', null=True),
            preserve_default=True,
        ),
    ]
