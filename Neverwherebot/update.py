# TODO use in locals() or just an else

import os
import threading
import imp
import datetime
import math
import re
import time
import Neverwherebot.models as models
import django.core.exceptions
from django.db.models.lookups import Day

threads = []


def start():
    startup_scripts()
    t = threading.Thread(target=update)
    threads.append(t)
    t.start()


def startup_scripts():

    this_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(this_dir, 'scripts')
    startup_dir = os.path.join(scripts_dir, 'startup')

    for f in os.listdir(startup_dir):
        if f.endswith('.py') and not f.startswith('_'):
            try:
                mod = imp.load_source(f[:-3], f)
                try:
                    mod.on_start()
                except:
                    print("Failed to execute on_start method for module %s." % f)
            except:
                print("Failed to import module %s." % f)

# TODO: Create seperate tick function feeding time to update
def update(hour, day):
    count = 0
    failed_count = 0
    failed = ()
    food_count = 0
    food_failed_count = 0
    food_failed = ()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(this_dir, 'scripts')

    scripts = enumerate_scripts(scripts_dir)
    characters = get_characters()
    acres = get_acres()
    storages = get_storages()
    cyclic_items = get_cyclical_items()

    for character in characters:
        update_recovery(character, hour)
        check_activity_queue(character, hour, day)

        if day in range(5):
            if update_jobs(character, scripts, scripts_dir, hour):
                count += 1
            else:
                failed_count += 1
                failed = failed + (character.name,)
                

        if hour == 12 or hour == 6 or hour == 18:
            if update_food(character):
                food_count += 1
            else:
                food_failed_count += 1
                food_failed = food_failed + (character.name,)

        if is_winter():
            check_for_freezing(character, hour)

    print("Successfully updated %s character jobs, %s failed, namely: %s" % (str(count), str(failed_count), str(failed)))
    if hour == 12:
        print("Successfully updated food for %s characters, %s failed, namely: %s" % (str(food_count), str(food_failed_count), str(food_failed)))

    for acre in acres:
        update_acre(acre, hour)  # Set growth and such

    for storage in storages:
        update_storage(storage)  # Check for spoilage etc
    if cyclic_items is not None:
        for item in cyclic_items:
            update_item(item)


def enumerate_scripts(scripts_dir):
    # Returns a directory with the directory's path name as key leading to a tuple of scripts
    scripts = {}
    for dirname, dirnames, filenames in os.walk(scripts_dir):
        scripts[dirname] = []
        for subdirname in dirnames:
            if subdirname != "startup":
                scripts = dict(scripts.items() + enumerate_scripts(subdirname).items())
        for filename in filenames:
            if filename.endswith('.py') and not filename.startswith('_'):
                scripts[dirname].append(filename)
    return scripts


def get_characters():
    return models.Character.objects.filter(deleted=False)  # Return a list of all character objects that are not marked
                                                           # as deleted


def get_acres():
    return models.Acre.objects.all()  # Returns a list of all acre objects


def get_storages():
    return models.Storage.objects.all()  # Returns a list of all storage objects


def get_cyclical_items():
    # return models.Item.objects.filter(cyclical=True)  # Returns a list of all items that are cyclical
    pass


def update_recovery(character, hour):
    # Checks whether the character is valid to recover HP or similar and does so if yes.
    if character.dead:
        return True
    if hour == 0:
        recover_hp(character.name, 1)
        
    recover_fp(character, 5)
    
    try:
        care = models.Caretaking.objects.get(patient=character)
        # Check type and do the appropriate things
    except:
        pass
    
    return True


def update_jobs(character, scripts, scripts_dir, hour):
    jobs = models.Employee.objects.filter(character=character)
    for job in jobs:
        if job.part == 1 and hour in range(8, 12) or job.part == 2 and hour in range(12, 16) or job.part == 0 and hour in range (8, 16):
            worksite = job.worksite
            if worksite is None:
                if job.current_activity == "craft":
                    if not exec_script("", "craft", 'update', character, job, hour):
                        return False
                else:
                    print("No worksite found for character %s job %s." % (character.name, str(job.part)))
                    return False
            elif os.path.isdir(os.path.join(scripts_dir, "worksites", worksite.type)):
                if job.current_activity == "craft":
                    if not exec_script("", "craft", 'update', character, job, hour):
                        return False
                elif not exec_script(os.path.join("worksites", worksite.type), job.job.name, 'update', character, job, hour):
                    return False
            else:
                print("Couldn't find script for %s, assuming it is a service job" % job.job.name)
                give_salary(character, job.part, hour)
    return True


def give_salary(character, part, hour):
    if hour == 11 and part == 1 or hour == 15 and part == 2 or hour == 15 and part == 0:
        employee = models.Employee.objects.filter(character=character).get(part=part)
        worksite = employee.worksite
        storage = worksite.storage
        storage_character = character.inventory
        money = remove_item("$", storage_name=storage.name, amount=employee.salary)
        if money == -1:
            money = 0
        add_item("$", storage_id=storage_character, amount=money)
        if money != employee.salary:
            print("Only delivered %s$ worth of money to %s for job %s, instead of %s" % (str(money), str(character.name), str(part), str(employee.salary)))
            message = "At %s, %s should have received a salary of %s$. Sadly your employer %s was unable to pay you and" \
                      " you only received %s$. This may be due to your employer running out of money, or" \
                      " a misconfiguration. You may want to contact him to resolve this issue." % (
                character.name, str(datetime.datetime.now()), str(employee.salary),
                worksite.owner.name, str(money),
            )

            send_message("", character.player.nick, message, flags='bwi')
            message = "At %s, your worksite %s failed to pay %s a fully salary due to a lack of funds in the" \
                      " main storage. You payed him %s, but should have payed him %s. Please transfer " \
                      "more funds to your worksite's storage, and pay your workers what you owe them." % (
                str(datetime.datetime.now()), worksite.name, character.name, str(money), str(employee.salary),
            )
            send_message("", worksite.owner.player.nick, message, flags="bwi")
        elif employee.salary != 0:
            message = "Today at %s, you received a salary of %s from your work at %s." % (
                str(datetime.datetime.now()), str(money), worksite.name,
            )
            send_message("", character.player.nick, message, flags="bw")
            message = "Today at %s, you payed %s %s$ for their work at %s" % (
                str(datetime.datetime.now()), character.name, str(money), worksite.name,
            )
            send_message("", worksite.owner.player.nick, message, flags="bw")


def remove_item(name, storage_name='', storage_id='', amount=1.0):
    # Returns how much, if any, was removed
    
    if amount == 0 or amount == 0.0:
        return 0.0
    
    if storage_name != '':
        try:
            storage = models.Storage.objects.get(name=storage_name)
        except:
            return "Storage not found."
    
    if storage_id != '':
        try:
            storage = models.Storage.objects.get(pk=storage_id)
        except:
            return "Storage not found."

    if storage_id == '' and storage_name == '':
        return -1
    
    try:
        item = models.Item.objects.filter(stored=storage).get(type=models.ItemType.objects.get(name=name))
    except:
        item = False
    if not not item:
        if item.amount - amount <= 0:
            deleted = item.amount
            try:
                item.delete()
            except:
                return "Failed to delete item."
            return deleted
        else:
            item.amount -= amount
            try:
                item.save()
            except:
                return "Failed to remove amount of item."
            return amount
    else:
        return "No item of that type in storage."


def add_item(name, storage_name='', storage_id='', amount=1.0, value='', worn=False):
    
    if amount == 0 or amount == 0.0:
        return True

    if storage_name != '':
        try:
            storage = models.Storage.objects.get(name=storage_name)
        except:
            return "Storage not found."

    if storage_id != '':
        try:
            storage = models.Storage.objects.get(pk=storage_id)
        except:
            return "Storage not found."

    if storage_id == '' and storage_name == '':
        return False
    
    try:
        item_type = models.ItemType.objects.get(name=name)
    except:
        return "Invalid ItemType."
    content = 0.0
    for i in models.Item.objects.filter(stored=storage):
            content += i.type.weight * i.amount
    if content + item_type.weight * amount > storage.size:
        return "Not enough room left in the storage."
    try:
        item = models.Item.objects.filter(stored=storage).get(type=item_type)
        item.amount += amount
        item.save()
        return True
    except:
        item = models.Item()
        item.type = item_type
        item.amount = amount
        item.stored = storage
        if value != '':
            item.value = value
        if worn:
            item.worn = True
        try:
            item.save()
        except:
            return "Failed to create item."
        return True


def is_item(name, storage_name='', storage_id='', amount=0):
    if storage_name != '':
        try:
            storage = models.Storage.objects.get(name=storage_name)
        except:
            return "Storage not found."

    if storage_id != '':
        try:
            storage = models.Storage.objects.get(pk=storage_id)
        except:
            return "Storage not found."

    if storage_id == '' and storage_name == '':
        return False
    
    try:
        item_type = models.ItemType.objects.get(name=name)
    except:
        return "Invalid ItemType."

    if models.Item.objects.filter(stored=storage).filter(type=item_type).exists():
        if models.Item.objects.filter(stored=storage).get(type=item_type).amount >= amount:
            return True
    return False



def update_food(character, day):
    # Checks the character's rations set, deducts food from his food storage or inventory,
    # or adjusts ration setting if necessary
    if character.rations == "Minimum":
        m = eat_meal(character, day, 600.0, 0.0, 0.0, 0.0)
        if m.calories < 600.0:
            message = "%s was unable to eat as much as he wanted on day %i. They wanted to eat " \
                    "at least 600kcal, but could only find %gkcal worth of food." % (character.name, day, m.calories)
            send_message("", character.player.nick, message, flags="bi")
        
    elif character.rations == "Half":
        m = eat_meal(character, day, 300.0, 0.0, 0.0, 0.0)
        if m.calories < 300.0:
            message = "%s was unable to eat as much as he wanted on day %i. They wanted to eat " \
                    "at least 300kcal, but could only find %gkcal worth of food." % (character.name, day, m.calories)
            send_message("", character.player.nick, message, flags="bi")
    
    elif character.rations == "Full":
        protein = 0.0
        vegetables = 0.0
        calories = 0.0
        fruit = 0.0
        for meal in models.Meal.objects.filter(character=character).filter(day__in=range(day-7, day)):
            calories += meal.calories
            vegetables += meal.vegetables
            protein += meal.protein
            fruit += meal.fruit
        calories = 14700.0 - calories
        protein = 2100.0 - protein
        vegetables = 1400.0 - vegetables
        fruit = 700.0 - fruit
        if calories > 1500.0:
            calories = 1500.0
        if (protein + vegetables + fruit) > 1500.0:
            while (protein + vegetables + fruit) > 1500.0:
                protein -= 1.0
                vegetables -= 1.0
                fruit -= 1.0
        m = eat_meal(character, day, 700.0 + calories, 100.0 + protein, 66.0 + vegetables, 33.0 + fruit)
        if m.calories < 700.0 or m.protein < 100.0 or m.vegetables < 66.0 or m.fruit < 33.0:
            message = "%s was unable to eat as much as he wanted on day %i." % (character.name, day)
            if m.calories < 700.0:
                message += " They wanted to eat at least 700kcal, but could only find %gkcal worth of food." % m.calories
            if m.protein < 100.0:
                message += " They wanted to eat at least 100kcal worth of meat, but could only find %gkcal worth of food." % m.protein
            if m.vegetables < 66.0:
                message += " They wanted to eat at least 66kcal worth of vegetables, but could only find %gkcal worth of food." % m.vegetables
            if m.fruit < 33.0:
                message += " They wanted to eat at least 33kcal worth of fruit, but could only find %gkcal worth of food." % m.fruit
            send_message("", character.player.nick, message, flags="bi")
    return True

        
def eat_meal(character, day, calories, p, v, f):
    left = calories
    protein = p
    vegetable = v
    fruit = f
    for i in models.Item.objects.filter(stored=character.foodstore).filter(type__in=models.ItemType.objects.filter(kcal__gt=0).exclude(flags__contains="p").exclude(flags__contains="v").exclude(flags__contains="f")):
        if left > (protein + vegetable + fruit):
            amount = (left - (protein + vegetable + fruit)) / i.type.kcal
            s = remove_item(i.type.name, storage_id=character.foodstore.pk, amount=amount)
            left -= s * i.type.kcal
    for i in models.Item.objects.filter(stored=character.foodstore).filter(type__in=models.ItemType.objects.filter(kcal__gt=0).exclude(flags__contains="v").exclude(flags__contains="f")):
        if protein > 0:
            amount = protein / i.type.kcal
            s = remove_item(i.type.name, storage_id=character.foodstore.pk, amount=amount)
            protein -= s * i.type.kcal
            left -= s * i.type.kcal
    for i in models.Item.objects.filter(stored=character.foodstore).filter(type__in=models.ItemType.objects.filter(kcal__gt=0).exclude(flags__contains="p").exclude(flags__contains="f")):
        if vegetable > 0:
            amount = vegetable / i.type.kcal
            s = remove_item(i.type.name, storage_id=character.foodstore.pk, amount=amount)
            vegetable -= s * i.type.kcal
            left -= s * i.type.kcal
    for i in models.Item.objects.filter(stored=character.foodstore).filter(type__in=models.ItemType.objects.filter(kcal__gt=0).exclude(flags__contains="p").exclude(flags__contains="v")):
        if fruit > 0:
            amount = fruit / i.type.kcal
            s = remove_item(i.type.name, storage_id=character.foodstore.pk, amount=amount)
            fruit -= s * i.type.kcal
            left -= s * i.type.kcal
    if left > 0:
        for i in models.Item.objects.filter(stored=character.foodstore).filter(type__in=models.ItemType.objects.filter(kcal__gt=0).exclude(flags__contains="p").exclude(flags__contains="v").exclude(flags__contains="f")):
            amount = left / i.type.kcal
            s = remove_item(i.type.name, storage_id=character.foodstore.pk, amount=amount)
            left -= s * i.type.kcal
    if left > 0:
        for i in models.Item.objects.filter(stored=character.foodstore).filter(type__in=models.ItemType.objects.filter(kcal__gt=0)):
            amount = left / i.type.kcal
            s = remove_item(i.type.name, storage_id=character.foodstore.pk, amount=amount)
            left -= s * i.type.kcal
            if "p" in i.type.flags:
                protein -= s * i.type.kcal
            if "v" in i.type.flags:
                vegetable -= s * i.type.kcal
            if "f" in i.type.flags:
                fruit -= s * i.type.kcal
    new = models.Meal()
    new.character = character
    new.day = day
    new.calories = calories - left
    new.protein = p - protein
    new.vegetables = v - vegetable
    new.fruit = f - fruit
    new.save()
    return new



def is_winter():
    day = get_current_day()
    year = math.floor(day / 360)
    day -= year * 360
    if day in range(271, 361):
        return True
    else:
        return False


def check_for_freezing(character, hour):
    pass  # Check severity of winter setting, modify by hour of day, check character housing, apply freezing problems


def send_message(sender, receiver, content, flags=''):
    # Flags: b = Sent by the Bot w = Work Related i = Important
    print("Reached update.")
    if not content:
        return "No content given."

    if sender != '':
        try:
            s = models.Player.objects.get(nick=sender)
        except django.core.exceptions.ObjectDoesNotExist:
            return "Sender could not be found."
        print("Sender found.")
    else:
        try:
            s = models.Player.objects.get(nick="Bot")
        except django.core.exceptions.ObjectDoesNotExist:
            return "Sender could not be found."
    try:
        r = models.Player.objects.get(nick=receiver)
    except django.core.exceptions.ObjectDoesNotExist:
        return "Receiver could not be found."

    if len(content) >= 10000:
        return "Message too long."

    m = models.Message(sender=s, receiver=r, message=content, flags=flags)
    m.save()
    return True


def get_current_day():
    return models.Game.objects.get(id=0).current_day


def get_skill(character, skill):
    
    try:
        char = models.Character.objects.get(name=character)
    except:
        return False
    if skill == "str":
        return char.str - 10
    elif skill == "dex":
        return char.dex - 10
    elif skill == "int":
        return char.int - 10
    elif skill == "vit":
        return char.vit - 10
    
    try:
        cs = models.CharacterSkill.objects.filter(character=char).get(skill=models.Skill.objects.get(name=skill))
        characterskill = cs.level
    except:
        characterskill = 0
    try:
        sk = models.Skill.objects.get(name=skill)
    except:
        return False
    if sk.attribute == "Str":
        att = characterskill + (char.str-10)
    elif sk.attribute == "Dex":
        att = characterskill + (char.dex-10)
    elif sk.attribute == "Int":
        att = characterskill + (char.int-10)
    elif sk.attribute == "Vit":
        att = characterskill + (char.vit-10)

    if sk.difficulty == "E":
        final = att - 2
    elif sk.difficulty == "A":
        final = att -4
    elif sk.difficulty == "H":
        final = att - 6
    elif sk.difficulty == "VH":
        final = att - 8

    return final


def update_acre(acre, hour):
    if hour != 15:
        return True
    if not acre.farm is None:
        farmer = False
        fail = False
        farm = acre.farm
        try:
            job = models.Job.objects.filter(worksite=farm).get(name="farmer")
        except:
            character = None
            fail = True
        try:
            employee = models.Employee.objects.filter(worksite=farm).get(job=job)
        except:
            character = None
            fail = True
        if not fail:
            character = employee.character
            farmer = True
    elif acre.owner:
        character = acre.owner
    else:
        character = None

    if models.Upgrade.objects.filter(acre=acre).exists():
        for upgrade in models.Upgrade.objects.filter(acre=acre):
            exec_script(os.path.join("acre", "upgrades"), upgrade.name, 'on_pre_update', acre)

    if acre.crop is not None:
        crop = acre.crop
        if acre.temperature not in crop.temperature_survive:
            growth_time = get_current_day() - acre.planted
            acre.growth_days = growth_time
            acre.save()
            if acre.temperature in crop.temperature_tolerate:
                acre.bonus -= 1
                acre.save()
            elif acre.temperature not in crop.temperature_good:
                if character:
                    message = "Your %s on acre %s is dying from the temperature! It usually tolerates %s, " \
                              "but the temperature on this acre is %s! They will die in a few days if nothing " \
                              "is done." % (crop.name_plural, acre.id, verbose_temperature_tolerance(crop),
                                            acre.temperature)
                    send_message("", character.name, message, "bwi")
                acre.bonus -= 10
                acre.save()

            if acre.humidity in crop.humidity_tolerate:
                acre.bonus -= 1
                acre.save()

            elif acre.humidity not in crop.humidity_good:
                if character:
                    message = "Your %s on acre %s is dying from the humidity! It usually tolerates %s, " \
                              "but the humidity on this acre is %s! They will die in a few days if nothing " \
                              "is done." % (crop.name_plural, acre.id, verbose_humidity_tolerance(crop),
                                            acre.temperature)
                    send_message("", character.name, message, "bwi")
                acre.bonus -= 10
                acre.save()

            if not farmer:
                last_30 = models.Tending.objects.filter(acre=acre).filter(day__in=range(get_current_day()-30, get_current_day()+1))
                if len(last_30) < 25:
                    acre.bonus -= 5
                    acre.save()

            if acre.growth_days == crop.time:
                acre.produce = crop.gross_yield * (1.0+(acre.bonus/100.0))
                if acre.fertility == "Barren":
                    acre.produce = int(acre.produce*0.1)
                elif acre.fertility == "Bad":
                    acre.produce = int(acre.produce*0.6)
                elif acre.fertility == "Fertile":
                    acre.produce = int(acre.produce*1.1)
                elif acre.fertility == "Very Fertile":
                    acre.produce = int(acre.prodce*1.3)
                acre.harvest_per = acre.produce / 40
                acre.save()
                if character is not None:
                    message = "Your acre %s is ready for harvest! Better do so soon or the yield will begin to " \
                              "rot." % acre.id
                    send_message("", character.name, message, "bwi")

            if acre.growth_days >= crop.time:
                if growth_time - crop.time == 7:
                    if character:
                        message = "Your acre %s has been ready for harvest for a week now, the fruits of your " \
                                  "labor are beginning to spoil! Harvest it quickly." % acre.id
                        send_message("", character.name, message, "bwi")
                if growth_time - crop.time > 7:
                    acre.produce *= 0.95
                    acre.save()

            if acre.bonus <= -100:
                if character:
                    message = "Disaster! Your %s on acre %s have withered away to nothingness! You will have " \
                              "to start over from scratch." % (crop.name_plural, acre.id)
                    send_message("", character.name, message, "bwi")
                acre.crop = None
                acre.pesticide = False
                acre.poisoned = False
                acre.tilled = 0
                acre.planted = None
                acre.harvest = 0
                acre.bonus = 0
                acre.harvest_per = 0
                acre.save()

            if acre.growth_days % 30 == 0:
                running = True
                count = 0
                while running:
                    found = False
                    try:
                        t = models.Tending.objects.filter(day=get_current_day()-count).get(acre=acre)
                        found = True
                    except:
                        pass
                    if count <= 30 and found:
                        acre.bonus += t.roll - crop.difficulty * 5
                        running = False
                    elif count > 30:
                        running = False
                    else:
                        count += 1
                acre.save()
    if models.Upgrade.objects.filter(acre=acre).exists():
        for upgrade in models.Upgrade.objects.filter(acre=acre):
            exec_script(os.path.join("acre", "upgrades"), upgrade.name, 'on_post_update', acre)


def verbose_temperature_tolerance(crop):
    result = ""
    wordlist = re.sub("[^\w]", " ",  crop.temperature_good + " " + crop.temperature_tolerate).split()
    if len(wordlist) > 1:
        for s in wordlist:
            result += s + " and"
    return result[:-4]


def verbose_humidity_tolerance(crop):
    result = ""
    wordlist = re.sub("[^\w]", " ",  crop.humidity_good + " " + crop.humidity_tolerate).split()
    if len(wordlist) > 1:
        for s in wordlist:
            result += s + " and"
    return result[:-4]


def exec_script(path, name, function, *args):
    f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts', path, name + ".py")
    if os.path.isfile(f):
        try:
            mod = imp.load_source(f[:-3], f)
            try:
                func = getattr(mod, function)
                return func(*args)
            except:
                print("Failed to execute %s method for module %s." % function, f)
                return False
        except:
            print("Failed to import module %s." % f)
            return False
        


def update_item(item):
    pass


def update_storage(storage):
    pass


def check_activity_queue(character, hour, day):
    queue = models.Activity.objects.filter(hour=hour).filter(day=day).filter(character=character)
    
    for a in queue:
        apply_activity(a)
    

def get_next_unbound(character):
    unbound = models.Activity.objects.filter(day=None).filter(hour=None).filter(character=character)
    if not unbound.exists():
        return None
    ret = None
    for a in unbound:
        if ret is None:
            ret = a
        else:
            if a.pk < ret.pk:
                ret = a
    return ret

    
def apply_activity(activity):
    if activity is None:
        return None
    if activity.activity is not None:
        activity.employment.activity = activity.activity
    if activity.acre is not None:
        activity.employment.acre = activity.acre
    if activity.craft is not None:
        activity.employment.craft = activity.craft
    if activity.tunnel is not None:
        activity.employment.tunnel = activity.tunnel
    if activity.process is not None:
        activity.employment.process = activity.process
    activity.employment.save()
    if not activity.persistant:
        activity.delete()
    return True
        
    
def deal_fp(character, fp, kind="", description=""):
    try:
        char = models.Character.objects.get(name=character)
    except:
        return "Character not found."
    
    current = char.fp
    for w in models.Wound.objects.filter(character=char).filter(kind="fp"):
        current -= w.damage
        
    if (current - fp) < 0:
        if current <= 0:
            deal_hp(character, fp, "s")
        else:
            deal_hp(character, fp - current, "s")
        if current - fp < -char.fp:
            fp = current + char.fp
            
    if fp == 0:
        return True
    
    if kind == "s":
        try:
            w = models.Wound.objects.filter(character=char).filter(kind="fp").get(flags="s")
            if w.damage > fp:
                try:
                    h = models.Wound.objects.filter(character=char).filter(kind="hp").get(flags="s")
                    recover_hp(character, w.damage - fp, "s")
                except:
                    pass
            w.damage = fp
            w.save()
            return True
        except:
            pass
    
    new = models.Wound()
    new.character = char
    new.kind = "fp"
    new.damage = fp
    new.description = description
    new.flags = kind
    new.save()
    return True 


def deal_hp(character, hp, kind="", location="", description=""):
    try:
        char = models.Character.objects.get(name=character)
    except:
        return "Character not found."
    
    if location != "":
        # Check for crippling
        pass
    
    # Check for death etc
    
    if kind == "s":
        try:
            w = models.Wound.objects.filter(character=char).filter(kind="hp").get(flags="s")
            w.damage = hp
            w.save()
            return True
        except:
            pass
    
    new = models.Wound()
    new.character = char
    new.kind = "hp"
    new.damage = hp
    new.description = description
    new.flags = kind
    new.location = location
    new.save()
    return True         

    
def recover_hp(character, hp, kind=""):
    try:
        char = models.Character.objects.get(name=character)
    except:
        return "Character not found."        
    
    if kind != "s" and kind != "u":
        for w in models.Wound.objects.filter(character=char).filter(kind="hp").exclude(flags__in=["u", "s"]):
            if hp > 0:
                w.damage -= hp
                if w.damage <= 0:
                    hp = -w.damage
                    w.delete()
                else:
                    w.save()
    elif kind == "s":
        w = models.Wound.objects.filter(character=char).filter(kind="hp").get(flags="s")
        w.damage -= hp
        w.save()
        hp = 0
    
    return hp # Return leftover HP not healed


def recover_fp(character, fp, kind=""):
    try:
        char = models.Character.objects.get(name=character)
    except:
        return "Character not found."        
    
    if kind != "s" and kind != "u":
        for w in models.Wound.objects.filter(character=char).filter(kind="fp").exclude(flags__in=["u", "s"]):
            if fp > 0:
                w.damage -= fp
                if w.damage <= 0:
                    fp = -w.damage
                    w.delete()
                else:
                    w.save()
    
    return fp
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




