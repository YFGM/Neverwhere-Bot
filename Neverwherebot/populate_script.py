import os, sys
from slugify import slugify
sys.path.append("/home/willie/Neverwhere-Bot")
sys.path.append("/home/willie/Neverwhere-Bot/Neverwherebot")
os.environ["DJANGO_SETTINGS_MODULE"] = "Neverwhere.settings"

import django
django.setup()

import Neverwherebot.models as models


def cs(name, difficulty, attribute):
    print "Attempting to create Skill %s" % name
    try:
        new = models.Skill(name=name, difficulty=difficulty, attribute=attribute, slug=slugify(name))
        new.save()
    except:
        print "Failed"
        return False
    print "Success."
    return True


def cp(name, category, full_name):
    if not "Weapon" in category:
        print "Attempting to create Perk %s." % name
        new = models.Perk(name=name, category=category, full_name=full_name)
        try:
            new.save()
        except:
            print "Failed."
            return False
        print "Success."
        return True
    else:
        WEAPON_CLASSES = (
        "Simple",
        "Axes",
        "Bows",
        "Claw Weapons",
        "Crossbows",
        "Exotic Weapons",
        "Heavy Blades",
        "Light Blades",
        "Maces and Hammers",
        "Polearms",
        "Slings and Thrown Weapons",
        "Spears and Lances",
        )
        for c in WEAPON_CLASSES:
            name = name + " " + slugify(c)
            print "Attempting to create Perk %s." % name
            new = models.Perk(name=name, category=category)
            try:
                new.save()
            except:
                print "Failed."
                return False
            print "Success."
            return True
            
            


# Basic Perks
cp("improved-hp", "Basic Tiered", "Improved HP")
cp("improved-fp", "Basic Tiered", "Improved FP")
cp("improved-melee-attack", "Basic Tiered", "Improved Melee Attack")
cp("improved-ranged-attack", "Basic Tiered", "Improved Ranged Attack")
cp("improved-will", "Basic Tiered", "Improved Will")
cp("improved-reaction", "Basic Tiered", "Improved Reaction")
cp("improved-fortitude", "Basic Tiered", "Improved Fortitude")
cp("improved-perception", "Basic Tiered", "Improved Perception")
cp("improved-basic-lift", "Basic Tiered", "Improved Basic Lift")

# Skills
s = "Str"
d = "Dex"
i = "Int"
v = "Vit"
e = "E"
a = "A"
h = "H"
vh = "VH"

cs("Acrobatics", e, d)
cs("Alchemy", vh, i)
cs("Artistry", a, d)
cs("Biology", h, i)
cs("Chemistry", h, i)
cs("Climbing", e, s)
cs("Disable Device", a, d)
cs("Engineering (Clockwork)", h, i)
cs("Engineering (Combat)", h, i)
cs("Engineering (Electric)", h, i)
cs("Engineering (Electronic)", h, i)
cs("Engineering (Mechanical)", h, i)
cs("Engineering (Mining)", h, i)
cs("Explosives (Demolition)", h, i)
cs("Explosives (Fireworks)", h, i)
cs("Explosives (Mining)", h, i)
cs("Farming", e, i)
cs("First Aid", e, i)
cs("Fishing", e, d)
cs("Flying", a, d)
cs("Glassblowing", a, d)
cs("Handle Animal", a, i)
cs("Herbalism", e, i)
cs("Hobby Skill", e, i)
cs("Leather Working", a, d)
cs("Martial Art", h, d)
cs("Masonry", a, d)
cs("Mechanic (Clockwork)", a, d)
cs("Mechanic (Combat)", a, d)
cs("Mechanic (Electric)", a, d)
cs("Mechanic (Electronic)", a, d)
cs("Mechanic (Mechanical)", a, d)
cs("Mechanic (Mining)", a, d)
cs("Mining", e, i)
cs("Physician", vh, i)
cs("Physics", vh, i)
cs("Pottery", a, d)
cs("Sense Motive", a, i)
cs("Sewing", a, d)
cs("Shiphandling (Ships)", a, i)
cs("Shiphandling (Airships)", a, i)
cs("Shiphandling (Submarine)", a, i)
cs("Sleight of Hand", a, d)
cs("Smithing (Weapons)", a, d)
cs("Smithing (Armor)", a, d)
cs("Smithing (General)", a, d)
cs("Smithing (Heavy)", a, d)
cs("Smithing (Fine)", a, d)
cs("Stealth", a, d)
cs("Surgery", vh, d)
cs("Survival", e, i)
cs("Swimming", e, s)
cs("Telekinesis", h, i)
cs("Thaumatology", vh, i)
cs("Woodworking (Carpentry)", a, d)
cs("Woodworking (Bowmaking)", a, d)
cs("Woodworking (Carving)", a, d)


# Skill Perks

cp(slugify("Acrobatics"), "Skill Tiered", "Acrobatics")
cp(slugify("Alchemy"),  "Skill Tiered", "Alchemy")
cp(slugify("Artistry"), "Skill Tiered", "Artistry")
cp(slugify("Biology"), "Skill Tiered", "Biology")
cp(slugify("Chemistry"), "Skill Tiered", "Chemistry")
cp(slugify("Climbing"), "Skill Tiered", "Climbing")
cp(slugify("Disable Device"), "Skill Tiered", "Disable Device")
cp(slugify("Engineering (Clockwork)"), "Skill Tiered", "Engineering (Clockwork)")
cp(slugify("Engineering (Combat)"), "Skill Tiered", "Engineering (Combat)")
cp(slugify("Engineering (Electric)"), "Skill Tiered", "Engineering (Electric)")
cp(slugify("Engineering (Electronic)"), "Skill Tiered", "Engineering (Electronic)")
cp(slugify("Engineering (Mechanical)"), "Skill Tiered", "Engineering (Mechanical)")
cp(slugify("Engineering (Mining)"), "Skill Tiered", "Engineering (Mining)")
cp(slugify("Explosives (Demolition)"), "Skill Tiered", "Explosives (Demolition)")
cp(slugify("Explosives (Fireworks)"), "Skill Tiered", "Explosives (Fireworks)")
cp(slugify("Explosives (Mining)"), "Skill Tiered", "Explosives (Mining)")
cp(slugify("Farming"), "Skill Tiered", "Farming")
cp(slugify("First Aid"), "Skill Tiered", "First Aid")
cp(slugify("Fishing"), "Skill Tiered", "Fishing")
cp(slugify("Flying"), "Skill Tiered", "Flying")
cp(slugify("Glassblowing"), "Skill Tiered", "Glassblowing")
cp(slugify("Handle Animal"), "Skill Tiered", "Handle Animal")
cp(slugify("Herbalism"), "Skill Tiered", "Herbalism")
cp(slugify("Hobby Skill"), "Skill Tiered", "Hobby Skill")
cp(slugify("Leather Working"), "Skill Tiered", "Leather Working")
cp(slugify("Martial Art"), "Skill Tiered", "Martial Art")
cp(slugify("Masonry"), "Skill Tiered", "Masonry")
cp(slugify("Mechanic (Clockwork)"), "Skill Tiered", "Mechanic (Clockwork)")
cp(slugify("Mechanic (Electric)"), "Skill Tiered", "Mechanic (Electric)")
cp(slugify("Mechanic (Electronic)"), "Skill Tiered", "Mechanic (Electronic)")
cp(slugify("Mechanic (Mechanical)"), "Skill Tiered", "Mechanic (Mechanical)")
cp(slugify("Mechanic (Mining)"), "Skill Tiered", "Mechanic (Mining)")
cp(slugify("Mining"), "Skill Tiered", "Mining")
cp(slugify("Physician"),  "Skill Tiered", "Physician")
cp(slugify("Physics"),  "Skill Tiered", "Physics")
cp(slugify("Pottery"), "Skill Tiered", "Pottery")
cp(slugify("Sense Motive"), "Skill Tiered", "Sense Motive")
cp(slugify("Sewing"), "Skill Tiered", "Sewing")
cp(slugify("Shiphandling (Ships)"), "Skill Tiered", "Shiphandling (Ships)")
cp(slugify("Shiphandling (Airships)"), "Skill Tiered", "Shiphandling (Airships)")
cp(slugify("Shiphandling (Submarines)"), "Skill Tiered", "Shiphandling (Submarines)")
cp(slugify("Sleight of Hand"), "Skill Tiered", "Sleight of Hand")
cp(slugify("Smithing (Weapons)"), "Skill Tiered", "Smithing (Weapons)")
cp(slugify("Smithing (Armor)"), "Skill Tiered", "Smithing (Armor)")
cp(slugify("Smithing (General)"), "Skill Tiered", "Smithing (General)")
cp(slugify("Smithing (Heavy)"), "Skill Tiered", "Smithing (Heavy)")
cp(slugify("Smithing (Fine)"), "Skill Tiered", "Smithing (Fine)")
cp(slugify("Stealth"), "Skill Tiered", "Stealth")
cp(slugify("Surgery"),  "Skill Tiered", "Surgery")
cp(slugify("Survival"), "Skill Tiered", "Survival")
cp(slugify("Swimming"), "Skill Tiered", "Swimming")
cp(slugify("Telekinesis"), "Skill Tiered", "Telekinesis")
cp(slugify("Thaumatology"),  "Skill Tiered", "Thaumatology")
cp(slugify("Woodworking (Carpentry)"), "Skill Tiered", "Woodworking (Carpentry)")
cp(slugify("Woodworking (Bowmaking)"), "Skill Tiered", "Woodworking (Bowmaking)")
cp(slugify("Woodworking (Carving)"), "Skill Tiered", "Woodworking (Carving)")


# Proficiency Perks
cp(slugify("Weapon Proficiency"), "Weapon", "Weapon Proficiency")
cp(slugify("Armor Proficiency (Light)"), "", "Armor Proficiency (Light)")
cp(slugify("Armor Proficiency (Medium)"), "", "Armor Proficiency (Medium)")
cp(slugify("Armor Proficiency (Heavy)"), "", "Armor Proficiency (Heavy)")


