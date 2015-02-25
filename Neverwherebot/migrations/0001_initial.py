# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(max_length=8192)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Acre',
            fields=[
                ('temperature', models.CharField(max_length=128, choices=[(b'H', b'Hot'), (b'N', b'Normal'), (b'CH', b'Chilly'), (b'C', b'Cold')])),
                ('humidity', models.CharField(max_length=128, choices=[(b'H', b'Humid'), (b'N', b'Normal'), (b'D', b'Dry'), (b'A', b'Arid')])),
                ('fertility', models.CharField(max_length=128, choices=[(b'BA', b'Barren'), (b'B', b'Bad'), (b'N', b'Normal'), (b'F', b'Fertile'), (b'VF', b'Very Fertile')])),
                ('irrigation', models.IntegerField()),
                ('intensity', models.IntegerField(default=0)),
                ('poisoned', models.BooleanField(default=False)),
                ('tilled', models.IntegerField(default=0)),
                ('planting', models.IntegerField(default=0)),
                ('planted', models.DateField(blank=True)),
                ('harvest', models.IntegerField(default=0)),
                ('harvest_per', models.IntegerField(default=0)),
                ('bonus', models.IntegerField(default=0)),
                ('id', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('produce', models.IntegerField(default=0)),
                ('growth_days', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part_time', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BaitEffect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('effect', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('capacity', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('sex', models.CharField(max_length=1)),
                ('str', models.IntegerField(default=10)),
                ('dex', models.IntegerField(default=10)),
                ('int', models.IntegerField(default=10)),
                ('vit', models.IntegerField(default=10)),
                ('hp', models.IntegerField()),
                ('fp', models.IntegerField()),
                ('san', models.IntegerField()),
                ('mab', models.IntegerField()),
                ('rab', models.IntegerField()),
                ('ac', models.IntegerField()),
                ('will', models.IntegerField()),
                ('re', models.DecimalField(max_digits=10, decimal_places=2)),
                ('fort', models.IntegerField()),
                ('per', models.IntegerField()),
                ('mo', models.IntegerField()),
                ('bl', models.DecimalField(max_digits=10, decimal_places=2)),
                ('current_HP', models.IntegerField()),
                ('current_FP', models.IntegerField()),
                ('current_san', models.IntegerField()),
                ('description', models.TextField(max_length=8192, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('house', models.ForeignKey(to='Neverwherebot.Building')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharacterPerk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot', models.IntegerField()),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharacterSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0)),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roll', models.IntegerField()),
                ('final', models.IntegerField()),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Craft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('difficulty', models.CharField(max_length=64, choices=[(b'S', b'Simple'), (b'A', b'Average'), (b'C', b'Complex'), (b'AM', b'Amazing')])),
                ('wr', models.CharField(max_length=32)),
                ('blueprint', models.CharField(blank=True, max_length=64, choices=[(b'S', b'Simple'), (b'A', b'Average'), (b'C', b'Complex'), (b'AM', b'Amazing')])),
                ('part_time', models.BooleanField(default=False)),
                ('take_10', models.BooleanField(default=False)),
                ('amount', models.IntegerField(default=1)),
                ('hours', models.IntegerField(default=0)),
                ('resources', models.IntegerField(default=0)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('name_plural', models.CharField(max_length=64)),
                ('temperature_good', models.CharField(max_length=64)),
                ('temperature_tolerate', models.CharField(max_length=64)),
                ('temperature_survive', models.CharField(max_length=64)),
                ('humidity_good', models.CharField(max_length=64)),
                ('humidity_tolerate', models.CharField(max_length=64)),
                ('difficulty', models.IntegerField()),
                ('gross_yield', models.IntegerField()),
                ('product_name', models.CharField(max_length=128, blank=True)),
                ('perennial', models.BooleanField(default=False)),
                ('seed', models.IntegerField()),
                ('time', models.IntegerField()),
                ('legume', models.BooleanField(default=False)),
                ('loss', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CropDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=8192)),
                ('crop', models.ForeignKey(to='Neverwherebot.Crop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisasterList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chance', models.IntegerField(default=1)),
                ('disaster', models.ForeignKey(to='Neverwherebot.Disaster')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part_time', models.BooleanField(default=False)),
                ('part', models.IntegerField(default=0, max_length=16)),
                ('salary', models.IntegerField(default=0)),
                ('current_activity', models.CharField(default=b'', max_length=64)),
                ('acre', models.ForeignKey(to='Neverwherebot.Acre', blank=True)),
                ('character', models.ForeignKey(to='Neverwherebot.Character')),
                ('craft', models.ForeignKey(to='Neverwherebot.Craft', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FishingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chance', models.IntegerField()),
                ('nat20', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForageList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chance', models.IntegerField()),
                ('nat20', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.IntegerField(default=0, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('interval', models.IntegerField(default=30)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('date_modifier', models.IntegerField(default=0)),
                ('winter_severity', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HerbList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chance', models.IntegerField()),
                ('nat20', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HuntingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chance', models.IntegerField()),
                ('nat20', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(default=1)),
                ('unit', models.CharField(max_length=64, blank=True)),
                ('value', models.IntegerField(blank=True)),
                ('worn', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('weight', models.IntegerField()),
                ('value', models.IntegerField()),
                ('flags', models.CharField(max_length=64, blank=True)),
                ('damage', models.CharField(blank=True, max_length=64, choices=[(b'B', b'Bludgeoning'), (b'P', b'Piercing'), (b'S', b'Slashing')])),
                ('ac', models.IntegerField(blank=True)),
                ('ap', models.IntegerField(blank=True)),
                ('re', models.IntegerField(blank=True)),
                ('wearable', models.BooleanField(default=False)),
                ('weapon_class', models.CharField(blank=True, max_length=64, choices=[(b'S', b'Simple'), (b'A', b'Axes'), (b'B', b'Bows'), (b'CW', b'Claw Weapons'), (b'C', b'Crossbows'), (b'EW', b'Exotic Weapons'), (b'HB', b'Heavy Blades'), (b'LB', b'Light Blades'), (b'M', b'Maces and Hammers'), (b'P', b'Polearms'), (b'ST', b'Slings and Thrown Weapons'), (b'SP', b'Speaks and Lances')])),
                ('bonus', models.IntegerField(blank=True)),
                ('el', models.IntegerField(blank=True)),
                ('kcal', models.IntegerField(blank=True)),
                ('spoils', models.IntegerField(blank=True)),
                ('herbal_uses', models.CharField(max_length=64, blank=True)),
                ('cyclical', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=64, choices=[(b'G', b'Gathering'), (b'C', b'Crafting'), (b'P', b'Processing'), (b'U', b'Unskilled'), (b'S', b'Service')])),
                ('description', models.TextField(max_length=8192)),
                ('default_salary', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_time', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(max_length=10000)),
                ('read', models.BooleanField(default=False)),
                ('flags', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MiningSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('depth', models.IntegerField()),
                ('description', models.TextField(max_length=8192, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('value', models.IntegerField()),
                ('poison', models.BooleanField(default=False)),
                ('native', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OreList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chance', models.IntegerField(default=1)),
                ('ore', models.ForeignKey(to='Neverwherebot.Ore')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('category', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(unique=True, max_length=128)),
                ('password', models.CharField(max_length=32)),
                ('op', models.BooleanField(default=False)),
                ('over_gm', models.BooleanField(default=False)),
                ('email', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hp', models.IntegerField(default=1)),
                ('ac', models.IntegerField(default=10)),
                ('escape', models.IntegerField(default=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('time', models.IntegerField()),
                ('required_building', models.ForeignKey(to='Neverwherebot.Building', null=True)),
                ('required_item', models.ForeignKey(to='Neverwherebot.ItemType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessInput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('multiplier', models.IntegerField(default=1)),
                ('item', models.ForeignKey(to='Neverwherebot.ItemType')),
                ('process', models.ForeignKey(to='Neverwherebot.Process')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessOutput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('multiplier', models.IntegerField(default=1)),
                ('item', models.ForeignKey(to='Neverwherebot.ItemType')),
                ('process', models.ForeignKey(to='Neverwherebot.Process')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('difficulty', models.CharField(max_length=128, choices=[(b'E', b'Easy'), (b'A', b'Average'), (b'H', b'Hard'), (b'VH', b'Very Hard')])),
                ('attribute', models.CharField(max_length=128, choices=[(b'Str', b'Strength'), (b'Dex', b'Dexterity'), (b'Int', b'Intelligence'), (b'Vit', b'Vitality')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('school', models.CharField(max_length=64)),
                ('classes', models.CharField(max_length=64)),
                ('fp_cost', models.IntegerField(default=1)),
                ('fp_cost_addendum', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('college', models.ForeignKey(to='Neverwherebot.College')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField(max_length=8192, blank=True)),
                ('size', models.IntegerField()),
                ('inventory', models.BooleanField(default=False)),
                ('allowed', models.ManyToManyField(to='Neverwherebot.Character', blank=True)),
                ('owner', models.ForeignKey(related_name='o', to='Neverwherebot.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField()),
                ('roll', models.IntegerField(blank=True)),
                ('acre', models.ForeignKey(to='Neverwherebot.Acre')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tunnel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quality', models.CharField(max_length=64, choices=[(b'P', b'Poor'), (b'A', b'Average'), (b'G', b'Good'), (b'GR', b'Great')])),
                ('richness', models.CharField(max_length=64, choices=[(b'G', b'Gold Rush'), (b'B', b'Bountiful'), (b'R', b'Rich'), (b'N', b'Normal'), (b'BA', b'Barren'), (b'RH', b'Red Herring'), (b'D', b'Dead')])),
                ('blueprint', models.BooleanField(default=False)),
                ('charge', models.ForeignKey(related_name='t', blank=True, to='Neverwherebot.Charge')),
                ('ore', models.ForeignKey(to='Neverwherebot.Ore')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upgrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('acre', models.ForeignKey(to='Neverwherebot.Acre', blank=True)),
                ('building', models.ForeignKey(to='Neverwherebot.Building', blank=True)),
                ('storage', models.ForeignKey(to='Neverwherebot.Storage', blank=True)),
                ('tunnel', models.ForeignKey(to='Neverwherebot.Tunnel', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Worksite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('type', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=8192, blank=True)),
                ('tree_modifier', models.IntegerField(default=1)),
                ('depth_dug', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(to='Neverwherebot.Character', blank=True)),
                ('storage', models.ForeignKey(to='Neverwherebot.Storage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='upgrade',
            name='worksite',
            field=models.ForeignKey(to='Neverwherebot.Worksite', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tunnel',
            name='worksite',
            field=models.ForeignKey(to='Neverwherebot.Worksite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tending',
            name='worksite',
            field=models.ForeignKey(to='Neverwherebot.Worksite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(to='Neverwherebot.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='s', to='Neverwherebot.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='process',
            field=models.ForeignKey(to='Neverwherebot.Process', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemtype',
            name='skill',
            field=models.ForeignKey(to='Neverwherebot.Skill', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='stored',
            field=models.ForeignKey(to='Neverwherebot.Storage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(to='Neverwherebot.ItemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='huntinglist',
            name='prey',
            field=models.ForeignKey(to='Neverwherebot.Prey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='huntinglist',
            name='site',
            field=models.ForeignKey(to='Neverwherebot.Worksite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='herblist',
            name='item',
            field=models.ForeignKey(to='Neverwherebot.ItemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='herblist',
            name='site',
            field=models.ForeignKey(to='Neverwherebot.Worksite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foragelist',
            name='item',
            field=models.ForeignKey(to='Neverwherebot.ItemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foragelist',
            name='site',
            field=models.ForeignKey(to='Neverwherebot.Worksite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fishinglist',
            name='itemtype',
            field=models.ForeignKey(to='Neverwherebot.ItemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='job',
            field=models.ForeignKey(to='Neverwherebot.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='tunnel',
            field=models.ForeignKey(to='Neverwherebot.Tunnel', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='worksite',
            field=models.ForeignKey(to='Neverwherebot.Worksite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crop',
            name='seed_type',
            field=models.ForeignKey(to='Neverwherebot.ItemType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='craft',
            name='item',
            field=models.ForeignKey(to='Neverwherebot.ItemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='craft',
            name='skill',
            field=models.ForeignKey(to='Neverwherebot.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='craft',
            name='worksite',
            field=models.ForeignKey(to='Neverwherebot.Worksite', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='charge',
            name='tunnel',
            field=models.ForeignKey(related_name='c', to='Neverwherebot.Tunnel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='characterskill',
            name='skill',
            field=models.ForeignKey(to='Neverwherebot.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='characterperk',
            name='perk',
            field=models.ForeignKey(to='Neverwherebot.Perk'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='inventory',
            field=models.ForeignKey(to='Neverwherebot.Storage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='player',
            field=models.ForeignKey(to='Neverwherebot.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='building',
            name='owner',
            field=models.ForeignKey(to='Neverwherebot.Character'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='building',
            name='storage',
            field=models.ForeignKey(to='Neverwherebot.Storage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baiteffect',
            name='fishing',
            field=models.ForeignKey(to='Neverwherebot.FishingList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='character',
            field=models.ForeignKey(to='Neverwherebot.Character'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(to='Neverwherebot.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='worksite',
            field=models.ForeignKey(to='Neverwherebot.Worksite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acre',
            name='crop',
            field=models.ForeignKey(to='Neverwherebot.Crop', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acre',
            name='farm',
            field=models.ForeignKey(to='Neverwherebot.Worksite', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acre',
            name='owner',
            field=models.ForeignKey(to='Neverwherebot.Character'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acre',
            name='pesticide',
            field=models.ForeignKey(to='Neverwherebot.ItemType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ability',
            name='character',
            field=models.ForeignKey(to='Neverwherebot.Character'),
            preserve_default=True,
        ),
    ]
