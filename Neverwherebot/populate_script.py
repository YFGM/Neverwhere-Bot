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


def cp(name, category):
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
cp("improved-hp", "Basic Tiered")
cp("improved-fp", "Basic Tiered")
cp("improved-melee-attack", "Basic Tiered")
cp("improved-ranged-attack", "Basic Tiered")
cp("improved-will", "Basic Tiered")
cp("improved-reaction", "Basic Tiered")
cp("improved-fortitude", "Basic Tiered")
cp("improved-perception", "Basic Tiered")
cp("improved-basic-lift", "Basic Tiered")

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
cs("Explosive (Demolition)", h, i)
cs("Explosive (Fireworks)", h, i)
cs("Explosive (Mining)", h, i)
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

cp(slugify("Acrobatics"), "Skill Tiered")
cp(slugify("Alchemy"),  "Skill Tiered")
cp(slugify("Artistry"), "Skill Tiered")
cp(slugify("Biology"), "Skill Tiered")
cp(slugify("Chemistry"), "Skill Tiered")
cp(slugify("Climbing"), "Skill Tiered")
cp(slugify("Disable Device"), "Skill Tiered")
cp(slugify("Engineering (Clockwork)"), "Skill Tiered")
cp(slugify("Engineering (Combat)"), "Skill Tiered")
cp(slugify("Engineering (Electric)"), "Skill Tiered")
cp(slugify("Engineering (Electronic)"), "Skill Tiered")
cp(slugify("Engineering (Mechanical)"), "Skill Tiered")
cp(slugify("Engineering (Mining)"), "Skill Tiered")
cp(slugify("Explosives (Demolition)"), "Skill Tiered")
cp(slugify("Explosives (Fireworks)"), "Skill Tiered")
cp(slugify("Explosives (Mining)"), "Skill Tiered")
cp(slugify("Farming"), "Skill Tiered")
cp(slugify("First Aid"), "Skill Tiered")
cp(slugify("Fishing"), "Skill Tiered")
cp(slugify("Flying"), "Skill Tiered")
cp(slugify("Glassblowing"), "Skill Tiered")
cp(slugify("Handle Animal"), "Skill Tiered")
cp(slugify("Herbalism"), "Skill Tiered")
cp(slugify("Hobby Skill"), "Skill Tiered")
cp(slugify("Leather Working"), "Skill Tiered")
cp(slugify("Martial Art"), "Skill Tiered")
cp(slugify("Masonry"), "Skill Tiered")
cp(slugify("Mechanic (Clockwork)"), "Skill Tiered")
cp(slugify("Mechanic (Combat)"), "Skill Tiered")
cp(slugify("Mechanic (Electric)"), "Skill Tiered")
cp(slugify("Mechanic (Electronic)"), "Skill Tiered")
cp(slugify("Mechanic (Mechanical)"), "Skill Tiered")
cp(slugify("Mechanic (Mining)"), "Skill Tiered")
cp(slugify("Mining"), "Skill Tiered")
cp(slugify("Physician"),  "Skill Tiered")
cp(slugify("Physics"),  "Skill Tiered")
cp(slugify("Pottery"), "Skill Tiered")
cp(slugify("Sense Motive"), "Skill Tiered")
cp(slugify("Sewing"), "Skill Tiered")
cp(slugify("Shiphandling (Ships)"), "Skill Tiered")
cp(slugify("Shiphandling (Airships)"), "Skill Tiered")
cp(slugify("Shiphandling (Submarine)"), "Skill Tiered")
cp(slugify("Sleight of Hand"), "Skill Tiered")
cp(slugify("Smithing (Weapons)"), "Skill Tiered")
cp(slugify("Smithing (Armor)"), "Skill Tiered")
cp(slugify("Smithing (General)"), "Skill Tiered")
cp(slugify("Smithing (Heavy)"), "Skill Tiered")
cp(slugify("Smithing (Fine)"), "Skill Tiered")
cp(slugify("Stealth"), "Skill Tiered")
cp(slugify("Surgery"),  "Skill Tiered")
cp(slugify("Survival"), "Skill Tiered")
cp(slugify("Swimming"), "Skill Tiered")
cp(slugify("Telekinesis"), "Skill Tiered")
cp(slugify("Thaumatology"),  "Skill Tiered")
cp(slugify("Woodworking (Carpentry)"), "Skill Tiered")
cp(slugify("Woodworking (Bowmaking)"), "Skill Tiered")
cp(slugify("Woodworking (Carving)"), "Skill Tiered")




