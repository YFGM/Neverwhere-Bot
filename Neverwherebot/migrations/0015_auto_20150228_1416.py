# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0014_auto_20150228_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='ac',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='ap',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='bonus',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='damage',
            field=models.CharField(blank=True, max_length=64, null=True, choices=[(b'B', b'Bludgeoning'), (b'P', b'Piercing'), (b'S', b'Slashing')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='el',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='flags',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='herbal_uses',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='kcal',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='re',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='spoils',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='unit',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='weapon_class',
            field=models.CharField(blank=True, max_length=64, null=True, choices=[(b'S', b'Simple'), (b'A', b'Axes'), (b'B', b'Bows'), (b'CW', b'Claw Weapons'), (b'C', b'Crossbows'), (b'EW', b'Exotic Weapons'), (b'HB', b'Heavy Blades'), (b'LB', b'Light Blades'), (b'M', b'Maces and Hammers'), (b'P', b'Polearms'), (b'ST', b'Slings and Thrown Weapons'), (b'SP', b'Speaks and Lances')]),
            preserve_default=True,
        ),
    ]
