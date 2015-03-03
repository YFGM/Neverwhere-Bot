# Interface.py
# Provides access to all core game world functionalities to external programs. Does NOT check any form of authentication

import imp
import os
import math

os.environ["DJANGO_SETTINGS_MODULE"] = "Neverwhere.settings"

import django
django.setup()

from slugify import slugify
import Neverwherebot.update as update
import Neverwherebot.models as model
import Neverwherebot.skill_perk as skill


def is_user(nick):
    if model.Player.objects.filter(nick=nick).exists():
        return True
    return False


def send_message(sender, receiver, content, flags=""):
    return update.send_message(sender, receiver, content, flags)


def get_messages(nick):
    ret = []
    try:
        p = model.Player.objects.get(nick=nick)
    except:
        return "Invalid player."

    me = model.Message.objects.filter(receiver=p)
    if not me.exists():
        return "No messages for user %s." % nick
    else:
        for m in me:
            ret.append([m.sender.nick, m.flags, m.sent_time.replace(tzinfo=None), m.read, m.message, m.pk])
    return ret


def get_message(message):
    try:
        m = model.Message.objects.get(pk=message)
    except:
        return "Message not found."

    ret = [m.sender.nick, m.flags, m.sent_time.replace(tzinfo=None), m.read, m.message, m.pk, m.receiver.nick]

    return ret


def delete_message(message):
    try:
        m = model.Message.objects.get(pk=message)
    except:
        return "Message could not be found."
    m.delete()
    return True


def set_message_read(message):
    try:
        m = model.Message.objects.get(pk=message)
    except:
        return "Message could not be found."

    m.read = True
    m.save()
    return True


def register(nick, pw=None, email=None):
    # Registers the given nick
    if model.Player.objects.filter(nick=nick):
        return "Player with this nick already exists."
    new = model.Player()
    new.nick = nick
    if pw:
        new.password = pw
    if email:
        new.email = email
    new.save()
    return True


def deregister(nick):
    pass


def create_character(player, name, sex, str, dex, int, vit):
    sex = sex.lower()
    if sex == "female":
        sex = "f"
    elif sex == "male":
        sex = "m"
    if model.Character.objects.filter(name=name).exists():
        return "Character with this name already exists."
    if sex == "mayonnaise":
        return "No Patrick, mayonnaise is not a gender."
    if not sex == "m" and not sex == "f":
        return "Invalid sex. Please use 'm' or 'f'."
    try:
        pl = model.Player.objects.get(nick=player)
    except:
        return "Invalid player."
    new = model.Character()
    new.player = pl
    new.name = name
    new.sex = sex
    new.str = str
    new.dex = dex
    new.int = int
    new.vit = vit
    new.current_HP = new.str
    new.current_FP = new.vit
    new.current_san = 100 + (new.int-10) * 10
    new.save()
    inv = model.Storage(owner=new)
    inv.name = name + "-Inventory"
    inv.size = new.str
    inv.inventory = True
    inv.save()
    new.inventory = inv
    new.save()
    recalculate_char(name)
    return True


def delete_character(name):
    character = model.Character.objects.filter(name=name)
    if not character:
        return "Character not found."
    if character.deleted:
        return "Character is already deleted."
    character.deleted = True
    character.save()


def is_owner(player, character):
    try:
        p = model.Player.objects.get(nick=player)
    except:
        return "Invalid player."
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."

    if char.player == p:
        return True
    else:
        return False


def add_perk(perk, character):
    s = recalculate_char(character)
    if isinstance(s, basestring):
        return s

    try:
        game = model.Game.objects.get(id=0)
    except:
        return "Game rules not found. This is a severe misconfiguration, please inform the Over GM of this bug."
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."

    old_hp = char.hp
    old_fp = char.fp
    old_san = char.san

    if perk.isdigit():
        try:
            p = model.Perk.objects.get(pk=perk)
        except:
            return "Perk not found."
    else:
        try:
            p = model.Perk.objects.get(name=perk)
        except:
            return "Perk not found."
    perks = update.get_current_day() / game.interval
    num = len(model.CharacterPerk.objects.filter(character=char))
    if num >= perks:
        return "No free perk slots available. %i perks available, %i taken." % (perks, num)
    
    can_take = True
    f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts', 'perks', slugify(p.name) + ".py")
    if os.path.isfile(f):
        try:
            mod = imp.load_source(f[:-3], f)
            try:
                P = mod.Perk()
                can_take = P.prerequisites(character)
            except:
                return "Failed to execute prerequisites module for perk %s." % p.name
        except:
            return "Failed to import module %s." % str(f)
    else:
        if not "Skill" in p.category:
            return "File %s not found." % str(f)

    if not can_take:
        return "Character does not fulfill the prerequisites for this perk."
    count = 0
    latest = 0
    if "Tiered" in p.category:
        for cp in model.CharacterPerk.objects.filter(character=char):
            if cp.perk == p:
                count += 1
                if cp.slot > latest:
                    latest = cp.slot
        if num + 1 > latest + count or count == 0:
            pass
        else:
            return "Character cannot take this perk at this moment due to Tiered restriction. The earliest they can take" \
                   " it is in %i perks." % ((latest + count + 1) - (num + 1))
    if not "Skill" in p.category:
        if not P.on_add(character):
            return "Error in 'on_add' function."
    else:
        s = skill.Perk()
        s.name = p.name
        if not s.on_add(character):
            return "Error in 'on_add' function."
    new = model.CharacterPerk()
    new.character = char
    new.perk = p
    new.slot = num + 1
    new.save()
    s = recalculate_char(character)
    if isinstance(s, basestring):
        return s
    char = model.Character.objects.get(name=character)
    inv = model.Storage.objects.get(name=char.name + "-Inventory")
    if old_hp != char.hp and old_hp is not None:
        char.current_HP += char.hp - old_hp
    if old_fp != char.fp and old_fp is not None:
        char.current_FP += char.fp - old_fp
    if old_san != char.san and old_san is not None:
        char.current_san += char.san - old_san
    if old_hp is None:
        char.current_HP = char.hp
    if old_fp is None:
        char.current_FP = char.fp
    if old_san is None:
        char.current_san = char.san
    char.save()
    inv.size += math.ceil(char.bl)
    inv.save()
    return True


def recalculate_char(character):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    if char.deleted:
        return "This character has been deleted."
    try:
        inv = model.Storage.objects.get(name=char.name + "-Inventory")
    except:
        return "Inventory not found, ya dun goofd."
    char.hp = char.str
    char.fp = char.vit
    char.will = char.int - 10
    char.san = 100 + (char.will * 10)
    char.mab = char.str - 10
    char.rab = char.dex - 10
    char.re = float(((char.dex - 10) + (char.vit - 10)) / 2)
    char.ac = 10 + math.ceil(char.re)
    char.fort = char.vit - 10
    char.per = char.int - 10
    char.mo = 4 + (char.re * 2)
    char.bl = (char.str**2)/10
    char.save()
    inv.size = 0
    inv.save()
    for cs in model.CharacterSkill.objects.filter(character=char):
        cs.level = 0
        cs.save()
    for n in range(1, len(model.CharacterPerk.objects.filter(character=char))+1):
        try:
            p = model.CharacterPerk.objects.filter(character=char).get(slot=n).perk
        except:
            continue
        if not "Skill" in p.category:
            f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts', 'perks', slugify(p.name) + ".py")
            if os.path.isfile(f):
                try:
                    mod = imp.load_source(f[:-3], f)
                    try:
                        P = mod.Perk()
                        P.on_recalc(character)
                    except:
                        return "Failed to execute on_recalc for perk %s." % p.name
                except:
                    return "Failed to import module %s." % str(f)
            else:
                return "Could not find perk script %s." % str(f)
        else:
            s = skill.Perk()
            s.name = p.name
            s.on_recalc(character)
    char = model.Character.objects.get(name=character)
    char.san = 100 + (char.will * 10)
    char.save()
    inv.size = char.bl * 10
    inv.save()
    return True


def add_item(item, storage, amount, value=0):
    return update.add_item(item, storage_name=storage, amount=amount, value=value)


def remove_item(item, storage, amount):
    return update.remove_item(item, storage_name=storage, amount=amount)


def get_item_type(item):
    try:
        i = model.ItemType.objects.get(name=item)
    except:
        return "ItemType not found."
    ret = {}
    ret["name"] = i.name
    ret["weight"] = i.weight
    ret["value"] = i.value
    ret["unit"] = i.unit
    ret["flags"] = i.flags
    return ret


def get_character(character):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    s = recalculate_char(char.name)
    if isinstance(s, basestring):
        return s
    ret = {}
    ret["sex"] = char.sex
    ret["str"] = char.str
    ret["dex"] = char.dex
    ret["int"] = char.int
    ret["vit"] = char.vit
    ret["hp"] = char.hp
    ret["fp"] = char.fp
    ret["will"] = char.will
    ret["san"] = char.san
    ret["mab"] = char.mab
    ret["rab"] = char.rab
    ret["ac"] = char.ac
    ret["re"] = char.re
    ret["fort"] = char.fort
    ret["per"] = char.per
    ret["mo"] = char.mo
    ret["bl"] = char.bl
    ret["current_hp"] = char.current_HP
    ret["current_fp"] = char.current_FP
    ret["current_san"] = char.current_san
    perks = {}
    for cp in model.CharacterPerk.objects.filter(character=char.pk):
        perks[cp.slot] = cp.perk.name
    ret["perks"] = perks
    skills = {}
    for cs in model.CharacterSkill.objects.filter(character=char.pk):
        skills[cs.skill.name] = update.get_skill(character, cs.skill.name)
    ret["skills"] = skills
    return ret


def get_perk_name(perk):
    name = perk
    try:
            p = model.Perk.objects.get(name=name)
    except:
        return "Could not find Perk %s." % name
    if "Skill" not in p.category:
        f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts', 'perks', name + ".py")
        if os.path.isfile(f):
            try:
                mod = imp.load_source(f[:-3], f)
                try:
                    P = mod.Perk()
                    return P.name
                except:
                    return "Failed to find name for perk %s." % name
            except:
                return "Failed to import module %s." % str(f)
        else:
            return "Could not find perk script %s." % str(f)
    else:
        s = model.Skill.objects.get(slug=name)
        return s.name


def get_current_character(player):
    try:
        p = model.Player.objects.get(nick=player)
    except:
        return "Player not found."
    return p.current_character.name


def set_current_character(player, character):
    try:
        p = model.Player.objects.get(nick=player)
    except:
        return "Player not found."
    try:
        c = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    
    p.current_character = c
    p.save()
    return True


def apply_job(worksite, job, character, parttime=False):
    pass


def remove_apply(character, worksite):
    pass


def remove_job(character, job):
    pass


def get_job(character):
    pass


def create_storage(character, name, size):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    s = model.Storage()
    s.name = name
    s.size = size
    s.owner = char
    try:
        s.save()
    except:
        return "Failed to create storage."
    return True


def get_storage(name):
    try:
        s = model.Storage.objects.get(name=name)
    except:
        return "Storage not found."
    ret = {}
    ret["name"] = s.name
    ret["size"] = s.size
    ret["description"] = s.description
    ret["inventory"] = s.inventory
    ret["owner"] = s.owner.name
    ret["allowed"] = []
    for c in s.allowed.all():
        ret["allowed"].append(c.name)
    return ret


def get_storage_contents(name):
    try:
        s = model.Storage.objects.get(name=name)
    except:
        return "Storage not found."
    ret = {}
    for i in model.Item.objects.filter(stored=s):
        ret[i.type.name] = (i.amount, i.type.unit)
    return ret


def set_storage_description(name, description):
    try:
        s = model.Storage.objects.get(name=name)
    except:
        return "Storage not found."
    if len(description) > 8192:
        return "Description too long."
    s.description = description
    s.save()
    return True


def store(character, storage, item, amount):
    s = update.remove_item(item, storage_name = character + "-Inventory", amount=amount)
    if isinstance(s, basestring):
        return s
    if s < 0:
        return "The amount must be a positive number."
    d = update.add_item(item, storage_name = storage, amount=s)
    if isinstance(d, basestring):
        b = update.add_item(item, storage_name = character + "-Inventory", amount=s)
        return d
    return s


def move(character, storage, item, amount, destination):
    pass


def storage_allow(character, storage):
    try:
        s = model.Storage.objects.get(name=storage)
    except:
        return "Storage not found."
    
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    
    s.allowed.add(char)
    try:
        s.save()
    except:
        return "Error adding allowed character."


def storage_disallow(character, storage):
    try:
        s = model.Storage.objects.get(name=storage)
    except:
        return "Storage not found."
    
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    if not char in s.allowed.all():
        return "Character not on allowed list."
    s.allowed.remove(char)
    try:
        s.save()
    except:
        return "Error removing allowed character."


def storage_steal(character, storage):
    pass


def storage_delete(storage):
    pass


def storage_remove(storage, item, amount):
    pass


def storage_resize(storage, size):
    try:
        s = model.Storage.objects.get(name=storage)
    except:
        return "Storage not found."
    if size < 0 or not isinstance(size, int):
        return "Size must be a positive integer."
    s.size = size
    try:
        s.save()
    except:
        return "Error resizing storage."


def storage_transfer(storage, recipient):
    pass


def storage_upgradte(storage, upgrade):
    pass


def worksite_create(character, type, name, storage, *args):
    pass


def get_worksite(worksite):
    pass


def delete_worksite(worksite):
    pass


def worksite_description(worksite, description):
    pass


def worksite_changestorage(worksite, storage):
    pass


def worksite_add(worksite, addition, *args):
    pass


def worksite_upgrade(worksite, upgrade, *args):
    pass


def worksite_hire(worksite, character, job, parttime=False):
    pass


def worksite_fire(worksite, character):
    pass


def worksite_salary(worksite, job, amount, money_store=None, frequency=None):
    pass


def create_job(worksite, job_name):
    pass