import os, sys
from slugify import slugify
sys.path.append("/home/willie/Neverwhere-Bot")
sys.path.append("/home/willie/Neverwhere-Bot/Neverwherebot")
os.environ["DJANGO_SETTINGS_MODULE"] = "Neverwhere.settings"

import django
django.setup()

import Neverwherebot.models as models


def cs(name, difficulty, attribute):
    try:
        new = models.Skill(name=name, difficulty=difficulty, attribute=attribute)
    except:
        return False
    new.save()
    return True


def cp(name, category):
    print "Attempting to create Perk %s." % name
    new = models.Perk(name=name, category=category)
    try:
        new.save()
    except:
        print "Failed."
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