from django.db import models

# Create your models here.


class Game(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(max_length=64)
    interval = models.IntegerField(default=30)
    start_date = models.DateField(auto_now_add=True)
    date_modifier = models.IntegerField(default=0)  # Added onto current date to determine time of year
    winter_severity = models.IntegerField(default=1)
    current_date = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Player(models.Model):
    nick = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=32)
    op = models.BooleanField(default=False)
    over_gm = models.BooleanField(default=False)
    email = models.CharField(max_length=128)
    current_character = models.ForeignKey("Character", related_name="p", null=True)

    def __str__(self):
        return self.nick


class Character(models.Model):
    player = models.ForeignKey("Player")
    name = models.CharField(max_length=64, unique=True)
    sex = models.CharField(max_length=1)
    str = models.IntegerField(default=10)
    dex = models.IntegerField(default=10)
    int = models.IntegerField(default=10)
    vit = models.IntegerField(default=10)
    hp = models.IntegerField(null=True)
    fp = models.IntegerField(null=True)
    san = models.IntegerField(null=True)
    mab = models.IntegerField(null=True)
    rab = models.IntegerField(null=True)
    ac = models.IntegerField(null=True)
    will = models.IntegerField(null=True)
    re = models.FloatField(null=True)
    fort = models.IntegerField(null=True)
    per = models.IntegerField(null=True)
    mo = models.IntegerField(null=True)
    bl = models.FloatField(null=True)
    current_HP = models.IntegerField()
    current_FP = models.IntegerField()
    current_san = models.IntegerField()
    inventory = models.ForeignKey("Storage", null=True)
    description = models.TextField(max_length=8192, blank=True)
    deleted = models.BooleanField(default=False)
    house = models.ForeignKey("Building", null=True)

    def __str__(self):
        return self.name


# TODO: Optional specialties
class Skill(models.Model):
    name = models.CharField(unique=True, max_length=64)
    DIFFICULTY_CHOICES = (
        ('E', 'Easy'),
        ('A', 'Average'),
        ('H', 'Hard'),
        ('VH', 'Very Hard')
    )
    difficulty = models.CharField(max_length=128, choices=DIFFICULTY_CHOICES)
    ATTRIBUTE_CHOICES = (
        ('Str', 'Strength'),
        ('Dex', 'Dexterity'),
        ('Int', 'Intelligence'),
        ('Vit', 'Vitality'),
    )
    attribute = models.CharField(max_length=128, choices=ATTRIBUTE_CHOICES)
    slug = models.CharField(max_length=128, unique=True, default="FIX ME")

    def __str__(self):
        return self.name


class CharacterSkill(models.Model):
    character = models.ForeignKey("Character")
    skill = models.ForeignKey("Skill")
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.character.name + ":" + self.skill.name


class Perk(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # Quirk, Flaw, Basic, Combat, Weapon, Skill, Magic, Spellcasting
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class CharacterPerk(models.Model):
    perk = models.ForeignKey("Perk")
    character = models.ForeignKey("Character")
    slot = models.IntegerField()

    def __str__(self):
        return self.character.name + ":" + self.perk.name + ":" + str(self.slot)



class Ability(models.Model):
    character = models.ForeignKey("Character")
    description = models.TextField(max_length=8192)


class Spell(models.Model):
    name = models.CharField(max_length=128, unique=True)
    school = models.CharField(max_length=64)   # TODO
    classes = models.CharField(max_length=64)  # TODO
    college = models.ForeignKey("College")
    fp_cost = models.IntegerField(default=1)
    fp_cost_addendum = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class College(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Acre(models.Model):
    owner = models.ForeignKey("Character")
    TEMPERATURE_CHOICES = (
        ("H", "Hot"),
        ("N", "Normal"),
        ("CH", "Chilly"),
        ("C", "Cold"),
    )
    temperature = models.CharField(choices=TEMPERATURE_CHOICES, max_length=128)
    HUMIDITY_CHOICES = (
        ("H", "Humid"),
        ("N", "Normal"),
        ("D", "Dry"),
        ("A", "Arid"),
    )
    humidity = models.CharField(choices=HUMIDITY_CHOICES, max_length=128)
    FERTILITY_CHOICES = (
        ("BA", "Barren"),
        ("B", "Bad"),
        ("N", "Normal"),
        ("F", "Fertile"),
        ("VF", "Very Fertile"),
    )
    fertility = models.CharField(choices=FERTILITY_CHOICES, max_length=128)
    irrigation = models.IntegerField()  # TODO
    pesticide = models.ForeignKey("ItemType", blank=True, null=True)
    intensity = models.IntegerField(default=0)
    poisoned = models.BooleanField(default=False)  # TODO
    crop = models.ForeignKey("Crop", blank=True, null=True)
    tilled = models.IntegerField(default=0)  # Increments towards 160, which is tilled
    planting = models.IntegerField(default=0)  # Increments towards 8 hours
    planted = models.IntegerField(blank=True, null=True)
    harvest = models.IntegerField(default=0)
    harvest_per = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    farm = models.ForeignKey("Worksite", blank=True, null=True)
    id = models.CharField(max_length=64, primary_key=True)
    produce = models.IntegerField(default=0)
    growth_days = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def reset(self):
        self.planted = None
        self.planting = 0
        self.crop = None
        self.harvest_per = 0
        self.harvest = 0
        self.bonus = 0
        self.produce = 0
        self.pesticide = None
        self.intensity = 0
        self.poisoned = False
        self.tilled = False
        self.growth_days = 0
        self.save()


class Worksite(models.Model):
    name = models.CharField(max_length=128, unique=True)
    owner = models.ForeignKey("Character", blank=True)
    type = models.CharField(max_length=128)
    description = models.TextField(max_length=8192, blank=True)
    storage = models.ForeignKey("Storage")
    tree_modifier = models.IntegerField(default=1)
    depth_dug = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Application(models.Model):
    character = models.ForeignKey("Character")
    worksite = models.ForeignKey("Worksite")
    job = models.ForeignKey("Job")
    part_time = models.BooleanField(default=False)
    employer_sent = models.BooleanField(default=False)
    sent = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.character.name + ":" + self.worksite.name


class Employee(models.Model):
    character = models.ForeignKey("Character")
    worksite = models.ForeignKey("Worksite")
    job = models.ForeignKey("Job")
    part_time = models.BooleanField(default=False)
    tunnel = models.ForeignKey("Tunnel", blank=True)
    part = models.IntegerField(max_length=16, default=0)
    craft = models.ForeignKey("Craft", blank=True)
    salary = models.IntegerField(default=0)
    current_activity = models.CharField(default="", max_length=64)
    acre = models.ForeignKey("Acre", blank=True)

    def __str__(self):
        return self.character.name + ":" + self.worksite.name


class Job(models.Model):
    name = models.CharField(max_length=64)
    TYPE_CHOICES = (
        ('G', "Gathering"),
        ('C', "Crafting"),
        ('P', "Processing"),
        ('U', "Unskilled"),
        ('S', "Service"),
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=64)
    description = models.TextField(max_length=8192)
    process = models.ForeignKey("Process", blank=True, null=True)
    default_salary = models.IntegerField(default=0)
    worksite = models.ForeignKey("Worksite")

    def __str__(self):
        return self.name


class Upgrade(models.Model):
    type = models.ForeignKey("UpgradeType")
    worksite = models.ForeignKey("Worksite", blank=True, null=True)
    tunnel = models.ForeignKey("Tunnel", blank=True, null=True)
    acre = models.ForeignKey("Acre", blank=True, null=True)
    storage = models.ForeignKey("Storage", blank=True, null=True)
    building = models.ForeignKey("Building", blank=True, null=True)

    def __str__(self):
        return self.type.name

class UpgradeType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    unique = models.BooleanField(default=False)
    slug = models.CharField(max_length=128)
    type = models.CharField(max_length=512)
    required_item = models.ForeignKey("ItemType")
    
    def __str__(self):
        return self.name
    

class HerbList(models.Model):
    site = models.ForeignKey("Worksite")
    item = models.ForeignKey("ItemType")
    chance = models.IntegerField()
    nat20 = models.BooleanField(default=False)

    def __str__(self):
        return self.site.name + ":" + self.item.name


class ForageList(models.Model):
    site = models.ForeignKey("Worksite")
    item = models.ForeignKey("ItemType")
    chance = models.IntegerField()
    nat20 = models.BooleanField(default=False)

    def __str__(self):
        return self.site.name + ":" + self.item.name


class HuntingList(models.Model):
    site = models.ForeignKey("Worksite")
    prey = models.ForeignKey("Prey")
    chance = models.IntegerField()
    nat20 = models.BooleanField(default=False)

    def __str__(self):
        return self.site.name + ":" + self.prey.item.name


class Prey(models.Model):
    name = models.CharField(max_length=128, default="Thingy", unique=True)
    hp = models.IntegerField(default=1)
    ac = models.IntegerField(default=10)
    escape = models.IntegerField(default=5)

    def __str__(self):
        return self.name


class FishingList(models.Model):
    itemtype = models.ForeignKey("ItemType")
    chance = models.IntegerField()
    nat20 = models.BooleanField(default=False)


class BaitEffect(models.Model):
    fishing = models.ForeignKey("FishingList")
    name = models.CharField(max_length=64)
    effect = models.IntegerField()

    def __str__(self):
        return self.name


class MiningSite(models.Model):
    name = models.CharField(max_length=128, unique=True)
    depth = models.IntegerField()
    description = models.TextField(max_length=8192, blank=True)

    def __str__(self):
        return self.name


class Tunnel(models.Model):
    worksite = models.ForeignKey("Worksite")
    QUALITY_CHOICES = (
        ('P', "Poor"),
        ('A', "Average"),
        ('G', "Good"),
        ('GR', "Great"),
    )
    quality = models.CharField(choices=QUALITY_CHOICES, max_length=64)
    RICHNESS_CHOICES = (
        ('G', "Gold Rush"),
        ('B', "Bountiful"),
        ('R', "Rich"),
        ('N', "Normal"),
        ('BA', "Barren"),
        ('RH', "Red Herring"),
        ('D', "Dead"),
    )
    richness = models.CharField(choices=RICHNESS_CHOICES, max_length=64)
    ore = models.ForeignKey("Ore")
    charge = models.ForeignKey("Charge", blank=True, related_name="t")
    blueprint = models.BooleanField(default=False)

    def __str__(self):
        return self.worksite.name


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
    tunnel = models.ForeignKey("Tunnel", related_name="c")

    def __str__(self):
        return self.tunnel.worksite.name


class Crop(models.Model):
    name = models.CharField(max_length=64, unique=True)
    name_plural = models.CharField(max_length=64)
    temperature_good = models.CharField(max_length=64)  # Not choices because multiple possible
    temperature_tolerate = models.CharField(max_length=64)
    temperature_survive = models.CharField(max_length=64)
    humidity_good = models.CharField(max_length=64)
    humidity_tolerate = models.CharField(max_length=64)
    difficulty = models.IntegerField()
    gross_yield = models.IntegerField()
    product_name = models.CharField(max_length=128, blank=True)
    perennial = models.BooleanField(default=False)
    seed = models.IntegerField()
    seed_type = models.ForeignKey("ItemType", blank=True)
    time = models.IntegerField()
    legume = models.BooleanField(default=False)
    loss = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CropDescription(models.Model):
    day = models.IntegerField(default=0)
    crop = models.ForeignKey("Crop")
    description = models.TextField(max_length=8192)

    def __str__(self):
        return self.crop.name


class Ore(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.IntegerField()
    poison = models.BooleanField(default=False)  # TODO
    native = models.BooleanField(default=False)  # TODO

    def __str__(self):
        return self.name


class Disaster(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Storage(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=8192, blank=True)
    owner = models.ForeignKey("Character", related_name="o")
    size = models.IntegerField()
    allowed = models.ManyToManyField("Character", blank=True)
    inventory = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=64)
    wr = models.CharField(max_length=32)
    blueprint = models.CharField(choices=DIFFICULTY_CHOICES, blank=True , max_length=64)
    part_time = models.BooleanField(default=False)
    take_10 = models.BooleanField(default=False)
    amount = models.IntegerField(default=1)
    hours = models.IntegerField(default=0)
    resources = models.IntegerField(default=0)
    worksite = models.ForeignKey("Worksite", blank=True)
    started = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.character.name + ":" + self.item.name


class Message(models.Model):
    sender = models.ForeignKey("Player", related_name="s")
    receiver = models.ForeignKey("Player")
    sent_time = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=10000)
    read = models.BooleanField(default=False)
    flags = models.CharField(max_length=64)

    def __str__(self):
        return self.sender.nick + ":" + self.receiver.nick


class Process(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # Input is taken times multiplier to get 1 unit, which produces
    # 1 unit multiplied by output.
    time = models.IntegerField()
    required_item = models.ForeignKey("ItemType", null=True)
    required_building = models.ForeignKey("Building", null=True)

    def __str__(self):
        return self.name


class ProcessInput(models.Model):
    process = models.ForeignKey("Process")
    item = models.ForeignKey("ItemType")
    multiplier = models.IntegerField(default=1)

    def __str__(self):
        return self.process.name + ":" + self.item.name


class ProcessOutput(models.Model):
    process = models.ForeignKey("Process")
    item = models.ForeignKey("ItemType")
    multiplier = models.IntegerField(default=1)

    def __str__(self):
        return self.process.name + ":" + self.item.name


class Item(models.Model):
    type = models.ForeignKey("ItemType")
    amount = models.FloatField(default=1.0)
    value = models.IntegerField(blank=True, null=True)
    worn = models.BooleanField(default=False)
    stored = models.ForeignKey("Storage")
    
    def __str__(self):
        return self.stored.name + ":" + self.type.name

# TODO: Move everything but flags to script class
class ItemType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    weight = models.IntegerField()
    value = models.IntegerField()
    unit = models.CharField(blank=True, max_length=64, null=True)
    flags = models.CharField(max_length=64, blank=True, null=True)
    DAMAGE_TYPES = (
        ('B', "Bludgeoning"),
        ('P', "Piercing"),
        ('S', "Slashing"),
    )
    damage = models.CharField(choices=DAMAGE_TYPES, blank=True, max_length=64, null=True)
    ac = models.IntegerField(blank=True, null=True)
    ap = models.IntegerField(blank=True, null=True)
    re = models.IntegerField(blank=True, null=True)
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
    weapon_class = models.CharField(choices=WEAPON_CLASSES, blank=True, max_length=64, null=True)
    bonus = models.IntegerField(blank=True, null=True)
    skill = models.ForeignKey("Skill", null=True, blank=True)
    el = models.IntegerField(blank=True, null=True)
    kcal = models.IntegerField(blank=True, null=True)
    spoils = models.IntegerField(blank=True, null=True)
    herbal_uses = models.CharField(blank=True, max_length=64, null=True)
    cyclical = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=128, unique=True)
    owner = models.ForeignKey("Character")
    capacity = models.IntegerField(default=1)
    storage = models.ForeignKey("Storage")

    def __str__(self):
        return self.name


class Tending(models.Model):
    worksite = models.ForeignKey("Worksite")
    day = models.IntegerField()
    roll = models.IntegerField(blank=True)
    acre = models.ForeignKey("Acre")

    def __str__(self):
        return self.worksite.name + ":" + self.acre.id