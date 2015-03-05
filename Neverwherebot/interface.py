# Interface.py
# Provides access to all core game world functionalities to external programs. Does NOT check any form of authentication

# TODO: Encumbrance(done), item bonuses, activity queue(should work), crafting(mostly done), jobs (farming(mostly done), mining, hunting, foraging, herbalism, fishing, lumber),
# buildings(simple), spell learning, rolling funcs, webinterface, content(items, buildings,
# prey, fish, perks, spells, crops, monsters)

import imp
import os
import math
import new

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
    if char.mo < 4:
        char.mo = 3
    char.save()
    inv.size = char.bl * 10
    inv.save()
    weight = 0
    for i in model.Item.objects.filter(stored=inv):
        weight += i.amount * i.type.weight
    if weight / char.bl > 6:
        char.mo = int(math.floor(char.mo*0.2))
        char.ac -= 5
    elif weight / char.bl > 3:
        char.mo = int(math.floor(char.mo*0.4))
        char.ac -= 3    
    elif weight / char.bl > 2:
        char.mo = int(math.floor(char.mo*0.6))
        char.ac -= 2
    elif weight / char.bl > 1:
        char.mo = int(math.floor(char.mo*0.8))
        char.ac -= 1
    char.save()
    return True


def add_item(item, storage, amount, value=0):
    r = update.add_item(item, storage_name=storage, amount=amount, value=value)
    if isinstance(r, basestring):
        return r
    s = model.Storage.objects.get(name=storage)
    if s.inventory:
        char = model.Character.objects.get(inv=s)
        recalculate_char(char)
    return r


def remove_item(item, storage, amount):
    r = update.remove_item(item, storage_name=storage, amount=amount)
    if isinstance(r, basestring):
        return r
    s = model.Storage.objects.get(name=storage)
    if s.inventory:
        char = model.Character.objects.get(inv=s)
        recalculate_char(char)
    return r


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
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Worksite not found."
    try:
        j = model.Job.objects.filter(worksite=w).get(name=job)
    except:
        return "Job not found."
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    
    try:
        a = model.Application.objects.filter(worksite=w).filter(character=char).filter(job=j).filter(employer_sent=False).get(part_time=parttime)
    except:
        try:
            a = model.Application.objects.filter(worksite=w).filter(character=char).filter(job=j).filter(employer_sent=True).get(part_time=parttime)
            part = 0
            if model.Employee.objects.filter(character=char).exists():
                if len(model.Employee.objects.filter(character=char)) == 1 and parttime:
                    if model.Employee.objects.get(character=char).part == 1:
                        part = 2
                    elif model.Employee.objects.get(character=char).part == 2:
                        part = 1
                else:
                    if not parttime:
                        if len(model.Employee.objects.filter(character=char)) == 2:
                            s = quit_job(character, 2)
                            if isinstance(s, basestring):
                                return s
                            s = quit_job(character, 1)
                            if isinstance(s, basestring):
                                return s
                        else:
                            s = quit_job(character)
                            if isinstance(s, basestring):
                                return s 
                    else:
                        if len(model.Employee.objects.filter(character=char)) == 2:
                            s = quit_job(character, 2)
                            if isinstance(s, basestring):
                                return s
                        else:
                            s = quit_job(character)
                            if isinstance(s, basestring):
                                return s 
                        
            new = model.Employee()
            new.character = char
            new.job = j
            new.worksite = w
            new.salary = j.default_salary
            new.part_time = parttime
            new.part = part
            new.save()
            a.delete()
            return True
        except:
            a = model.Application()
            a.character = char
            a.job = j
            a.employer_sent = False
            a.part_time = parttime
            a.worksite = w
            a.save()
            if not parttime:
                message = "%s has asked to work at %s as a %s. To accept, do " \
                "!worksite hire %s %s %s" % (char.name, w.name, j.name, w.name, char.name, j.name)
            else:
                message = "%s has asked to work at %s as a %s part time. To accept, do " \
                "!worksite hire %s %s %s -p" % (char.name, w.name, j.name, w.name, char.name, j.name)
            update.send_message(char.player.nick, w.owner.player.nick, message)
            return "An application has been sent."
    return "An application has already been sent."
    

def remove_apply(character, worksite):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Worksite not found."
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    
    a = model.Application.objects.filter(character=char).filter(worksite=w)
    if a.exists():
        for p in a:
            p.delete()
        return True
    else:
        return "No applications to delete."


def quit_job(character, job=0):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    try:
        j = model.Employee.objects.filter(character=char).get(part=job)
    except:
        if job == 0:
            j = model.Employee.objects.filter(character=char)
            if j.exists():
                for e in j:
                    e.delete()
                return True
        else:      
            return "You aren't working at that time of day."
    
    j.delete()
    return True


def get_job(character):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    ret = []
    j = model.Employee.objects.filter(character=char)
    if j.exists():
        for e in j:
            emp = {}
            emp["worksite"] = e.worksite.name
            emp["job"] = e.job.name
            emp["parttime"] = e.part_time
            emp["tunnel"] = e.tunnel.pk
            emp["part"] = e.part
            emp["craft"] = e.craft.pk
            emp["salary"] = e.salary
            emp["current_activity"] = e.current_activity
            emp["acre"] = e.acre.id
            ret.append(emp)
    return ret


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
    d = update.add_item(item, storage_name = storage, amount=s)
    if isinstance(d, basestring):
        update.add_item(item, storage_name = character + "-Inventory", amount=s)
        return d
    return s


def move(storage, item, amount, destination):
    s = update.remove_item(item, storage_name = storage, amount=amount)
    if isinstance(s, basestring):
        return s
    d = update.add_item(item, storage_name = destination, amount=s)
    if isinstance(d, basestring):
        update.add_item(item, storage_name = storage, amount=s)
        return d
    return s


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
    try:
        store = model.Storage.objects.get(name=storage)
    except:
        return "Storage not found."
    for i in model.Item.objects.filter(stored=store):
        i.delete()
    store.delete()
    return True


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
    try:
        s = model.Storage.objects.get(name=storage)
    except:
        return "Storage not found."
        
    try:
        char = model.Character.objects.get(name=recipient)
    except:
        return "Character not found."
    
    s.owner = char
    s.save()
    return True

def storage_upgrade(storage, upgrade):
    pass


def worksite_create(character, type, name, storage, *args):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Cannot find character."
    try:
        store = model.Storage.objects.get(name=storage)
    except:
        return "Storage not found."
    if type not in ["farm", "mine", "craft", "wilderness", "other"]:
        return "Invalid worksite type."
    
    new = model.Worksite()
    new.name = name
    new.owner = char
    new.storage = store
    new.type = type
    try:
        new.save()
    except:
        return "Failed to create worksite."
    if type == "farm":
        create_job(name, "farmer", type="G")
        create_job(name, "farmhand", type="U")
    if type == "mine":
        create_job(name, "overseer", type="G")
        create_job(name, "miner", type="U")
    if type == "craft":
        create_job(name, "craft", type="C")
    if type == "wilderness":
        create_job(name, "hunter", type="G")
        create_job(name, "forager", type="G")
        create_job(name, "fisher", type="G")
        create_job(name, "herbalist", type="G")
        create_job(name, "lumberjack", type="G")
    return True


def get_worksite(worksite):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    ret = {}
    ret["description"] = w.description
    ret["owner"] = w.owner.name
    ret["storage"] = w.storage.name
    ret["type"] = w.type
    ret["tree"] = w.tree_modifier
    ret["depth"] = w.depth_dug
    ret["employees"] = {}
    for c in model.Employee.objects.filter(worksite=w):
        ret["employees"][c.character.name] = c.job.name
    return ret


def delete_worksite(worksite):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    w.delete()
    return True


def worksite_description(worksite, description):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    w.description = description
    w.save()
    return True


def worksite_changestorage(worksite, storage):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    try:
        store = model.Storage.objects.get(name=storage)
    except:
        return "Cannot find storage."
    w.storage = store
    w.save()
    return True


def worksite_add(worksite, addition, *args):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    
    if not w.type == "farm":
        return "This worksite is not a farm."
    
    try:
        acre = model.Acre.objects.get(id=addition)
    except:
        return "Cannot find acre."
    
    acre.farm = w
    acre.save()
    return True


def get_acre(id):
    try:
        a = model.Acre.objects.get(id=id)
    except:
        return "Acre cannot be found."
    ret = {}
    ret["owner"] = a.owner.name
    ret["fertility"] = a.fertility
    ret["temperature"] = a.temperature
    ret["humidity"] = a.humidity
    if a.crop is not None:
        ret["crop"] = a.crop.name
    else:
        ret["crop"] = None
    ret["tilled"] = a.tilled
    ret["planting"] = a.planting
    ret["planted"] = a.planted
    ret["harvest"] = a.harvest
    ret["harvest_per"] = a.harvest_per
    ret["bonus"] = a.bonus
    if a.farm is not None:
        ret["farm"] = a.farm.name
    else:
        ret["farm"] = None
    ret["produce"] = a.produce
    ret["growth_days"] = a.growth_days
    return ret
    

def worksite_upgrade(worksite, upgrade, *args):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    try:
        u = model.UpgradeType.objects.get(name=upgrade)
    except:
        return "Cannot find upgrade type."
    
    if model.Upgrade.objects.filter(worksite=w).filter(type=u).exists() and u.unique:
        return "This upgrade can only be applied once."
    
    if w.type not in u.type:
        return "This upgrade cannot be applied to this type of worksite."
    
    new = model.Upgrade()
    new.worksite = w
    new.type = u
    new.save()
    return True


def worksite_hire(worksite, character, job, parttime=False):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Cannot find character."
    try:
        j = model.Job.objects.filter(worksite=w).get(name=job)
    except:
        return "Cannot find job."
    
    try:
        a = model.Application.objects.filter(worksite=w).filter(character=char).filter(job=j).filter(employer_sent=False).get(part_time=parttime)
    except:
        try:
            a = model.Application.objects.filter(worksite=w).filter(character=char).filter(job=j).filter(employer_sent=True).get(part_time=parttime)
            return "An invitation has already been sent."
        except:
            a = model.Application()
            a.character = char
            a.job = j
            a.employer_sent = True
            a.part_time = parttime
            a.worksite = w
            a.save()
            if not parttime:
                message = "%s has invited you to work at %s as a %s. To accept, do " \
                "!job apply %s %s" % (w.owner.name, w.name, j.name, w.name, j.name)
            else:
                message = "%s has invited you to work at %s as a %s part time. To accept, do " \
                "!job apply %s %s -p" % (w.owner.name, w.name, j.name, w.name, j.name)
            update.send_message(w.owner.player.nick, char.player.nick, message)
            return "An invitation has been sent."
    part = 0
    if model.Employee.objects.filter(character=char).exists():
        if len(model.Employee.objects.filter(character=char)) == 1 and parttime:
            if model.Employee.objects.get(character=char).part == 1:
                part = 2
            elif model.Employee.objects.get(character=char).part == 2:
                part = 1
        else:
            if not parttime:
                if len(model.Employee.objects.filter(character=char)) == 2:
                    s = quit_job(character, 2)
                    if isinstance(s, basestring):
                        return s
                    s = quit_job(character, 1)
                    if isinstance(s, basestring):
                        return s
                else:
                    s = quit_job(character)
                    if isinstance(s, basestring):
                        return s 
            else:
                if len(model.Employee.objects.filter(character=char)) == 2:
                    s = quit_job(character, 2)
                    if isinstance(s, basestring):
                        return s
                else:
                    s = quit_job(character)
                    if isinstance(s, basestring):
                        return s 
    new = model.Employee()
    new.character = char
    new.job = j
    new.worksite = w
    new.salary = j.default_salary
    new.part_time = parttime
    new.part = part
    new.save()
    a.delete()
    return True

def worksite_fire(worksite, character):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Cannot find character."
    
    try:
        e = model.Employee.objects.filter(character=char).get(worksite=w)
    except:
        return "Character does not work at that worksite."
    e.delete()
    return True 


def worksite_salary(worksite, job, amount, money_store=None, frequency=None):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    try:
        j = model.Job.objects.filter(worksite=w).get(name=job)
    except:
        return "Cannot find job."
    j.default_salary = amount
    j.save()
    return True


def create_job(worksite, job_name, type="S"):
    try:
        w = model.Worksite.objects.get(name=worksite)
    except:
        return "Cannot find worksite."
    try:
        j = model.Job.objects.filter(worksite=worksite).get(name=job_name)
        return "Job of that name already exists."
    except:
        j = model.Job()
        j.worksite = w
        j.name = job_name
        j.type = type
        j.save()
        return True
    

def get_upgrade(upgrade):
    try:
        u = model.UpgradeType.objects.get(name=upgrade)
    except:
        return "Upgrade type not found."
    ret = {}
    ret["unique"] = u.unique
    ret["item"] = u.required_item.name
    ret["slug"] = u.slug
    ret["type"] = u.type
    return ret        
        
        
#TODO: Activity queue for part time 
def craft_start(character, item_name, skill_name, difficulty, worksite_name=None, job=0, take_10=False, amount=1):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    try:
        item = model.ItemType.objects.get(name=item_name)
    except:
        return "Item not found."
    try:
        skill = model.Skill.objects.get(name=skill_name)
    except:
        return "Skill not found."
    worksite = None
    if worksite_name is not None:
        try:
            worksite = model.Worksite.objects.get(name=worksite_name)
        except:
            return "Worksite not found."
    employment = None
    if model.Employee.objects.filter(character=char).exists():
        if len(model.Employee.objects.filter(character=char)) == 1:
            employment = model.Employee.objects.get(character=char)
        else:
            try:
                employment = model.Employee.objects.filter(character=char).get(part=job)
            except:
                return "Failed to get employment."

    
    new = model.Craft()
    new.character = char
    new.item = item
    new.skill = skill
    if difficulty.lower() == "s":
        new.difficulty = "Simple"
    elif difficulty.lower() == "a":
        new.difficulty = "Average"
    elif difficulty.lower() == "c":
        new.difficulty = "Complex"
    else:
        new.difficulty = "Amazing"
    new.take_10 = take_10
    new.amount = amount
    new.worksite = worksite
    new.started = update.get_current_day()
    new.save()
    
    if employment is None:
        cj = model.Employee()
        cj.character = char
        cj.craft = new
        cj.worksite = worksite
        cj.part = job
        cj.current_activity = "craft"
        cj.save()
    else:
        if employment.current_activity == "craft":
            queue_activity(character, job, activity="craft", craft=new.pk)
        else:
            employment.craft = new
            employment.current_activity = "craft"
            employment.save()
    return True
        
        
def queue_activity(character, job=None, activity=None, acre=None, craft=None, tunnel=None, day=None, hour=None, process=None):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Character not found."
    if job is not None:
        try:
            e = model.Employee.objects.filter(character=char).get(part=job)
        except:
            return "Employment not found."
    else:
        e = None
    new = model.Activity()
    new.character = char
    new.employment = e
    new.activity = activity
    new.hour = hour
    new.day = day
    if acre is not None:
        try:
            a = model.Acre.objects.get(id=acre)
            new.acre = a
        except:
            return "Acre not found."
    if craft is not None:
        try:
            c = model.Craft.objects.get(pk=craft)
            new.craft = c
        except:
            return "Craft not found."
    if tunnel is not None:
        try:
            t = model.Acre.objects.get(pk=tunnel)
            new.tunnel = t
        except:
            return "Tunnel not found."
    if process is not None:
        try:
            p = model.Process.objects.get(pk=process)
        except:
            return "Process not found."
    new.save()
    return True    
            
        
def craft_cancel(id):
    try:
        craft = model.Craft.objects.get(pk=id)
    except:
        return "Cannot find craft."
        
    if model.Employee.objects.filter(craft=craft).filter(current_activity="craft").exists():
        for e in model.Employee.objects.filter(craft=craft):
            e.current_activity = ""
            e.save()
            if e.worksite is None:
                e.delete()
    craft.delete()
    return True


def get_crafts(character):
    try:
        char = model.Character.objects.get(name=character)
    except:
        return "Cannot find Character."
    
    ret= {}
    for e in model.Employee.objects.filter(character=char):
        if e.craft is not None:
            craft = {}
            craft["id"] = e.craft.pk
            craft["item"] = e.craft.item.name
            craft["skill"] = e.craft.skill.name
            craft["difficulty"] = e.craft.difficulty
            craft["blueprint"] = e.craft.blueprint
            craft["take_10"] = e.craft.take_10
            craft["amount"] = e.craft.amount
            craft["hours"] = e.craft.hours
            craft["worksite"] = e.craft.worksite.name
            craft["started"] = e.craft.started
            ret[e.pk] = craft
    return ret


def get_craft(id):
    try:
        c = model.Craft.objects.get(pk=id)
    except:
        return "Craft not found."
    craft = {}
    craft["id"] = c.pk
    craft["item"] = c.item.name
    craft["skill"] = c.skill.name
    craft["difficulty"] = c.difficulty
    craft["blueprint"] = c.blueprint
    craft["take_10"] = c.take_10
    craft["amount"] = c.amount
    craft["hours"] = c.hours
    if c.worksite is not None:
        craft["worksite"] = c.worksite.name
    else:
        craft["worksite"] = None
    craft["started"] = c.started
    craft["character"] = c.character.name
    return craft

    
def set_t10(craft, flip=True, set=False):
    try:
        c = model.Craft.objects.get(pk=craft)
    except:
        return "Craft not found."
    if flip:
        c.take_10 = not c.take_10
        c.save()
    else:
        c.take_10 = set
        c.save()
    return True
        
        
def tick():
    try:
        g = model.Game.objects.get(id=0)
    except:
        return "Game rules not found. This is a severe misconfiguration."
    update.update(g.current_hour+1, g.current_day % 7)
    g.current_hour += 1
    if g.current_hour == 24:
        g.current_hour = 0
        g.current_day += 1
    g.save()
    return True
        
        
def get_time():
    try:
        g = model.Game.objects.get(id=0)
    except:
        return "Game rules not found. This is a severe misconfiguration."
    ret = {}
    ret["hour"] = g.current_hour
    ret["day"] = g.current_day
    return ret
        
    
        
    
    