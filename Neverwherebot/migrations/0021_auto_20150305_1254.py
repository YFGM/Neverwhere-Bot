# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0020_auto_20150305_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='acre',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Acre', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='craft',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Craft', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='tunnel',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Tunnel', null=True),
            preserve_default=True,
        ),
    ]
