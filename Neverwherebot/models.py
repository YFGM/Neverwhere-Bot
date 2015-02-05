from django.db import models

# Create your models here.


class Game(models.Model):
    name = models.CharField()
    interval = models.IntegerField(default=30)
    start_date = models.DateField(auto_now_add=True)
    date_modifier = models.IntegerField(default=0)  # Added onto current date to determine time of year
    winter_severity = models.IntegerField(default=1)


class Player(models.Model):
    nick = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=32)
    op = models.BooleanField(default=False)
    over_gm = models.BooleanField(default=False)


class Character(models.Model):
    player = models.ForeignKey("Player")
    name = models.CharField(max_length=64, unique=True)
    str = models.IntegerField(default=10)
    dex = models.IntegerField(default=10)
    int = models.IntegerField(default=10)
    vit = models.IntegerField(default=10)
    hp = models.IntegerField()
    fp = models.IntegerField()
    san = models.IntegerField()
    mab = models.IntegerField()
    rab = models.IntegerField()
    ac = models.IntegerField()
    will = models.IntegerField()
    re = models.DecimalField()
    fort = models.IntegerField()
    per = models.IntegerField()
    mo = models.IntegerField()
    bl = models.DecimalField()
    current_HP = models.IntegerField()
    current_FP = models.IntegerField()
    current_san = models.IntegerField()
    perks = models.ManyToManyField("Perk")
    inventory = models.ForeignKey("Storage")
    description = models.TextField(max_length=8192, blank=True)
    deleted = models.BooleanField(default=False)
    house = models.ForeignKey("Building")


class Skill(models.Model):
    name = models.CharField(unique=True)
    DIFFICULTY_CHOICES = (
        'E',
        'A',
        'H',
        'VH',
    )
    difficulty = models.CharField(max_length=128, choices=DIFFICULTY_CHOICES)
    ATTRIBUTE_CHOICES = (
        'Str',
        'Dex',
        'Int',
        'Vit',
    )
    attribute = models.CharField(max_length=128, choices=ATTRIBUTE_CHOICES)


class CharacterSkill(models.Model):
    character = models.ForeignKey("Character")
    skill = models.ForeignKey("Skill")
    level = models.IntegerField(default=0)


class Perk(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # Quirk, Flaw, Basic, Combat, Weapon, Skill, Magic, Spellcasting
    category = models.CharField()
    prerequisites = models.ForeignKey("Prerequisite")


class Prerequisite(models.Model):
    str = models.IntegerField()
    dex = models.IntegerField()
    int = models.IntegerField()
    vit = models.IntegerField()
    mab = models.IntegerField()
    rab = models.IntegerField()
    will = models.IntegerField()
    re = models.DecimalField()
    fort = models.IntegerField()
    per = models.IntegerField()
    mo = models.IntegerField()
    bl = models.DecimalField()
    perks = models.ManyToManyField("Perk")


class Ability(models.Model):
    character = models.ForeignKey("Character")
    description = models.TextField(max_length=8192)


class Spell(models.Model):
    name = models.CharField(max_length=128, unique=True)
    school = models.CharField()   # TODO
    classes = models.CharField()  # TODO
    college = models.ForeignKey("College")
    fp_cost = models.IntegerField(default=1)
    fp_cost_addendum = models.CharField()
    description = models.TextField()


class College(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Acre(models.Model):
    owner = models.ForeignKey("Character")
    TEMPERATURE_CHOICES = (
        "Hot",
        "Normal",
        "Chilly",
        "Cold",
    )
    temperature = models.CharField(choices=TEMPERATURE_CHOICES)
    HUMIDITY_CHOICES = (
        "Humid",
        "Normal",
        "Dry",
        "Arid",
    )
    humidity = models.CharField(choices=HUMIDITY_CHOICES)
    FERTILITY_CHOICES = (
        "Barren",
        "Bad",
        "Normal",
        "Fertile",
        "Very Fertile",
    )
    fertility = models.CharField(choices=FERTILITY_CHOICES)
    irrigation = models.IntegerField()  # TODO
    fertilizer = models.IntegerField(default=0)  # 0 = None, 1 = Nitrogen, 2 = N/P/K
    pesticide = models.BooleanField(default=False)
    poisoned = models.BooleanField(defaukt=False)  # TODO
    crop = models.ForeignKey("Crop", blank=True)
    tilled = models.IntegerField(default=0)  # Increments towards 8, which is tilled
    planted = models.DateField(blank=True)
    harvest = models.IntegerField(default=0)
    harvest_per = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    farm = models.ForeignKey("Worksite", blank=True)
    id = models.CharField(max_length=64)
    produce = models.IntegerField(default=0)
    growth_days = models.IntegerField(default=0)


class Worksite(models.Model):
    name = models.CharField(max_length=128, unique=True)
    owner = models.ForeignKey("Character", blank=True)
    type = models.CharField()
    description = models.TextField(max_length=8192, blank=True)
    storage = models.ForeignKey("Storage")
    tree_modifier = models.IntegerField(default=1)
    depth_dug = models.IntegerField(default=0)


class Application(models.Model):
    character = models.ForeignKey("Character")
    worksite = models.ForeignKey("Worksite")
    job = models.ForeignKey("Job")
    part_time = models.BooleanField(default=False)


class Employee(models.Model):
    character = models.ForeignKey("Character")
    worksite = models.ForeignKey("Worksite")
    job = models.ForeignKey("Job")
    part_time = models.BooleanField(default=False)
    tunnel = models.ForeignKey("Tunnel", blank=True)
    part = models.IntegerField(max_length=16, default=0)
    craft = models.ForeignKey("Craft", blank=True)
    salary = models.IntegerField(default=0)
    current_activity = models.CharField(default="")


class Job(models.Model):
    name = models.CharField(max_length=64)
    TYPE_CHOICES = (
        ('G', "Gathering"),
        ('C', "Crafting"),
        ('P', "Processing"),
        ('U', "Unskilled"),
        ('S', "Service"),
    )
    type = models.CharField(choices=TYPE_CHOICES)
    description = models.TextField(max_length=8192)
    process = models.ForeignKey("Process", blank=True)
    default_salary = models.IntegerField()


class Upgrade(models.Model):
    name = models.CharField(max_length=128)
    worksite = models.ForeignKey("Worksite", blank=True)
    tunnel = models.ForeignKey("Tunnel", blank=True)
    acre = models.ForeignKey("Acre", blank=True)
    storage = models.ForeignKey("Storage", blank=True)
    building = models.ForeignKey("Building", blank=True)


class HerbList(models.Model):
    site = models.ForeignKey("Worksite")
    item = models.ForeignKey("ItemType")
    chance = models.IntegerField()
    nat20 = models.BooleanField()


class ForageList(models.Model):
    site = models.ForeignKey("Worksite")
    item = models.ForeignKey("ItemType")
    chance = models.IntegerField()
    nat20 = models.BooleanField()


class HuntingList(models.Model):
    site = models.ForeignKey("Worksite")
    prey = models.ForeignKey("Prey")
    chance = models.IntegerField()
    nat20 = models.BooleanField()


class Prey(models.Model):
    hp = models.IntegerField(default=1)
    ac = models.IntegerField(default=10)
    escape = models.IntegerField(default=5)


class FishingList(models.Model):
    itemtype = models.ForeignKey("ItemType")
    chance = models.IntegerField()
    nat20 = models.BooleanField()


class BaitEffect(models.Model):
    fishing = models.ForeignKey("FishingList")
    name = models.CharField(max_length=64)
    effect = models.IntegerField()


class MiningSite(models.Model):
    name = models.CharField(max_length=128, unique=True)
    depth = models.IntegerField()
    description = models.TextField(max_length=8192, blank=True)


class Tunnel(models.Model):
    worksite = models.ForeignKey("Worksite")
    QUALITY_CHOICES = (
        ('P', "Poor"),
        ('A', "Average"),
        ('G', "Good"),
        ('GR', "Great"),
    )
    quality = models.CharField(choices=QUALITY_CHOICES)
    RICHNESS_CHOICES = (
        ('G', "Gold Rush"),
        ('B', "Bountiful"),
        ('R', "Rich"),
        ('N', "Normal"),
        ('BA', "Barren"),
        ('RH', "Red Herring"),
        ('D', "Dead"),
    )
    richness = models.CharField(choices=RICHNESS_CHOICES)
    ore = models.ForeignKey("Ore")
    charge = models.ForeignKey("Charge", blank=True)
    blueprint = models.BooleanField(default=False)


class OreList(models.Model):
    ore = models.ForeignKey("Ore")
    chance = models.IntegerField(default=1)


class DisasterList(models.Model):
    disaster = models.ForeignKey("Disaster")
    chance = models.IntegerField(default=1)


class Charge(models.Model):
    roll = models.IntegerField()
    final = models.IntegerField()
    character = models.ForeignKey("Character")
    tunnel = models.ForeignKey("Tunnel")


class Crop(models.Model):
    name = models.CharField(max_length=64, unique=True)
    name_plural = models.CharField(max_length=64)
    temperature_good = models.CharField()  # Not choices because multiple possible
    temperature_tolerate = models.CharField()
    temperature_survive = models.CharField()
    humidity_good = models.CharField()
    humidity_tolerate = models.CharField()
    difficulty = models.IntegerField()
    gross_yield = models.IntegerField()
    product_name = models.CharField(max_length=128, blank=True)
    perennial = models.BooleanField()
    seed = models.IntegerField()
    seed_type = models.ForeignKey("ItemType", blank=True)
    time = models.IntegerField()
    legume = models.BooleanField()
    loss = models.BooleanField()


class CropDescription(models.Model):
    day = models.IntegerField(default=0)
    crop = models.ForeignKey("Crop")
    description = models.TextField(max_length=8192)


class Ore(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.IntegerField()
    poison = models.BooleanField()  # TODO
    native = models.BooleanField()  # TODO


class Disaster(models.Model):
    name = models.CharField(max_length=128)


class Storage(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=8192, blank=True)
    owner = models.ForeignKey("Character")
    size = models.IntegerField()
    allowed = models.ManyToManyField("Character", blank=True)
    inventory = models.BooleanField(default=False)


class Craft(models.Model):
    character = models.ForeignKey("Character")
    item = models.ForeignKey("ItemType")
    skill = models.ForeignKey("Skill")
    value = models.IntegerField()
    DIFFICULTY_CHOICES = (
        ('S', "Simple"),
        ('A', "Average"),
        ('C', "Complex"),
        ('AM', "Amazing"),
    )
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES)
    wr = models.CharField(max_length=32)
    blueprint = models.CharField(choices=DIFFICULTY_CHOICES, blank=True)
    part_time = models.BooleanField()
    take_10 = models.BooleanField()
    amount = models.IntegerField(default=1)
    hours = models.IntegerField(default=0)
    resources = models.IntegerField(default=0)
    worksite = models.ForeignKey("Worksite", blank=True)
    started = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey("Player")
    receiver = models.ForeignKey("Player")
    sent_time = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=10000)
    read = models.BooleanField(default=False)
    flags = models.CharField()


class Process(models.Model):
    name = models.CharField(max_length=128, unique=True)
    base = models.ForeignKey("ItemType")
    out = models.ForeignKey("ItemType")
    loss = models.IntegerField()
    time = models.IntegerField()


class Item(models.Model):
    type = models.ForeignKey("ItemType")
    amount = models.IntegerField(default=1)
    unit = models.CharField(blank=True)
    value = models.IntegerField(blank=True)
    worn = models.BooleanField(default=False)
    stored = models.ForeignKey("Storage")


class ItemType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    weight = models.IntegerField()
    value = models.IntegerField()
    flags = models.CharField(max_length=64, blank=True)
    DAMAGE_TYPES = (
        ('B', "Bludgeoning"),
        ('P', "Piercing"),
        ('S', "Slashing"),
    )
    damage = models.CharField(choices=DAMAGE_TYPES, blank=True)
    ac = models.IntegerField(blank=True)
    ap = models.IntegerField(blank=True)
    re = models.IntegerField(blank=True)
    wearable = models.BooleanField(default=False)
    WEAPON_CLASSES = (
        ('S', "Simple"),
        ('A', "Axes"),
        ('B', "Bows"),
        ('CW', "Claw Weapons"),
        ('C', "Crossbows"),
        ('EW', "Exotic Weapons"),
        ('HB', "Heavy Blades"),
        ('LB', "Light Blades"),
        ('M', "Maces and Hammers"),
        ('P', "Polearms"),
        ('ST', "Slings and Thrown Weapons"),
        ('SP', "Speaks and Lances"),
    )
    weapon_class = models.CharField(choices=WEAPON_CLASSES, blank=True)
    bonus = models.IntegerField(blank=True)
    skill = models.ForeignKey("Skill", blank=True)
    el = models.IntegerField(blank=True)
    kcal = models.IntegerField(blank=True)
    spoils = models.IntegerField(blank=True)
    herbal_uses = models.CharField(blank=True, max_length=64)
    cyclical = models.BooleanField(default=False)


class Building:
    name = models.CharField(max_length=128, unique=True)
    owner = models.ForeignKey("Character")
    capacity = models.IntegerField(default=1)
    storage = models.ForeignKey("Storage")


class Tending(models.Model):
    worksite = models.ForeignKey("Worksite")
    day = models.IntegerField()
    roll = models.IntegerField(blank=True)
    acre = models.ForeignKey("Acre")