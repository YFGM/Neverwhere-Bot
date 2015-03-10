# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0025_character_rations'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='foodstore',
            field=models.ForeignKey(related_name='f', to='Neverwherebot.Storage', null=True),
            preserve_default=True,
        ),
    ]
