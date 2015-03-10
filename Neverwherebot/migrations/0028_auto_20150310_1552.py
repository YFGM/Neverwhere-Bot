# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Neverwherebot', '0027_perk_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caretaking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=64)),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('roll', models.IntegerField()),
                ('caretaker', models.ForeignKey(to='Neverwherebot.Employee')),
                ('patient', models.ForeignKey(to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField()),
                ('calories', models.FloatField()),
                ('protein', models.FloatField(default=0)),
                ('vegetables', models.FloatField(default=0)),
                ('fruit', models.FloatField(default=0)),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=3)),
                ('damage', models.IntegerField()),
                ('location', models.CharField(max_length=64, null=True)),
                ('flags', models.CharField(default=b'', max_length=64)),
                ('description', models.CharField(default=b'', max_length=1024)),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='character',
            name='dead',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='deathflag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
