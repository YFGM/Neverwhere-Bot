# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0019_auto_20150305_1216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='current_date',
            new_name='current_day',
        ),
        migrations.RemoveField(
            model_name='game',
            name='date_modifier',
        ),
        migrations.RemoveField(
            model_name='game',
            name='start_date',
        ),
        migrations.AddField(
            model_name='game',
            name='current_hour',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
