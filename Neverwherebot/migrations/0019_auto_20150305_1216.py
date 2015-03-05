# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0018_auto_20150304_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='craft',
            name='part_time',
        ),
        migrations.AlterField(
            model_name='craft',
            name='blueprint',
            field=models.CharField(blank=True, max_length=64, null=True, choices=[(b'S', b'Simple'), (b'A', b'Average'), (b'C', b'Complex'), (b'AM', b'Amazing')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='craft',
            name='started',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='craft',
            name='worksite',
            field=models.ForeignKey(blank=True, to='Neverwherebot.Worksite', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='craft',
            name='wr',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
