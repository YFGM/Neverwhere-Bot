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


def update():
    count = 0
    failed_count = 0
    failed = ()
    food_count = 0
    food_failed_count = 0
    food_failed = ()
    hour = datetime.datetime.now().hour
    day = datetime.datetime.now().day

    this_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(this_dir, 'scripts')

    scripts = enumerate_scripts(scripts_dir)
    characters = get_characters()
    acres = get_acres()
    storages = get_storages()
    cyclic_items = get_cyclical_items()

    for character in characters:
        update_recovery(character, hour)

        if workday():
            if update_jobs(character, scripts, scripts_dir, hour):
                count += 1
            else:
                failed_count += 1
                failed = failed + (character.name + ": " + character.job.name)

        if hour == 12:
            if update_food(character):
                food_count += 1
            else:
                food_failed_count += 1
                food_failed = food_failed + (character.name + ": " + character.job.name)

        if is_winter():
            check_for_freezing(character, hour)

    print("Successfully updated %s character jobs, %s failed, namely: %s" % (str(count), str(failed_count), str(failed)))
    if hour == 12:
        print("Successfully updated food for %s characters, %s failed, namely: %s" % (str(food_count), str(food_failed_count), str(food_failed)))

    for acre in acres:
        update_acre(acre, hour)  # Set growth and such

    for storage in storages:
        update_storage(storage)  # Check for spoilage etc

    for item in cyclic_items:
        update_item(item)

    time.sleep(3600)


def enumerate_scripts(scripts_dir):
    # Returns a directory with the directory's path name as key leading to a tuple of scripts
    scripts = {}
    for dirname, dirnames, filenames in os.walk(scripts_dir):
        scripts[dirname] = ()
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
    return models.Item.objects.filter(cyclical=True)  # Returns a list of all items that are cyclical


def update_recovery(character, hour):
    pass  # Checks whether the character is valid to recover HP or similar and does so if yes.


def update_jobs(character, scripts, scripts_dir, hour):
    jobs = models.Employee.objects.filter(character=character.pk)
    for job in jobs:
        if job.part == 1 and hour in range(8, 12) or job.part == 2 and hour in range(12, 16) or job.part == 0 and hour in range (8, 16):
            worksite = models.Worksite.objects.filter(pk=job.worksite)
            if not worksite.exists():
                if job.type == "craft":
                    if not exec_script("", "craft", 'update', character, job, hour):
                        return False
                else:
                    print("No worksite found for character %s job %s." % (character.name, str(job.part)))
                    return False
            elif os.path.join(scripts_dir, worksite.type) in scripts:
                if not exec_script(os.path.join("worksites", worksite.type), job.name, 'update', character, job, hour):
                    return False
                else:
                    print("Couldn't find script for %s, assuming it is a service job" % job.name)
                    give_salary(character, job.part, hour)
    return True


def give_salary(character, part, hour):
    if hour == 11 and part == 1 and workday() or hour == 15 and part == 2 and workday() or hour == 15 and part == 0 and workday():
        employee = models.Employee.objects.filter(character=character.pk).filter(part=part)
        worksite = models.Worksite.objects.filter(pk=employee.worksite)
        storage = models.Storage.objects.filter(pk=worksite.storage)
        storage_character = models.Storage.objects.filter(pk=character.inventory)
        money = remove_item("$", storage_id=storage, amount=employee.salary)
        if money == -1:
            money = 0
        add_item("$", storage_id=storage_character, amount=money)
        if money != employee.salary:
            print("Only delivered %s$ worth of money to %s for job %s, instead of %s" % (str(money), str(character.name), str(part), str(employee.salary)))
            message = "At %s, %s should have received a salary of %s$. Sadly your employer %s was unable to pay you and" \
                      " you only received %s$. This may be due to your employer running out of money, or" \
                      " a misconfiguration. You may want to contact him to resolve this issue." % (
                character.name, str(datetime.datetime.now()), str(employee.salary),
                models.Character.objects.filter(pk=worksite.owner).name, str(money),
            )

            send_message("", models.Player.objects.filter(pk=character.player).nick, message, flags='bwi')
            message = "At %s, your worksite %s failed to pay %s a fully salary due to a lack of funds in the" \
                      " main storage. You payed him %s, but should have payed him %s. Please transfer " \
                      "more funds to your worksite's storage, and pay your workers what you owe them." % (
                str(datetime.datetime.now()), worksite.name, character.name, str(money), str(employee.salary),
            )
            send_message("", models.Player.objects.filter(pk=models.Character.objects.filter(pk=worksite.owner).player).nick, message, flags="bwi")
        elif employee.salary != 0:
            message = "Today at %s, you received a salary of %s from your work at %s." % (
                str(datetime.datetime.now()), str(money), worksite.name,
            )
            send_message("", models.Player.objects.filter(pk=character.player).nick, message, flags="bw")
            message = "Today at %s, you payed %s %s$ for their work at %s" % (
                str(datetime.datetime.now()), character.name, str(money), worksite.name,
            )
            send_message("", models.Player.objects.filter(pk=models.Character.objects.filter(pk=worksite.owner).player).nick, message, flags="bw")


def workday():
    if datetime.datetime.today() in range(5):
        return True
    else:
        return False


def remove_item(name, storage_name='', storage_id='', amount=1):
    # Returns how much, if any, was removed
    if storage_name != '':
        storage = models.Storage.objects.filter(name=storage_name)

    if storage_id != '':
        storage = models.Storage.objects.filter(pk=storage_id)

    if storage_id == '' and storage_name == '':
        return -1

    item = models.Item.objects.filter(stored=storage.pk).filter(name=name)

    if item.exists():
        if item.amount - amount <= 0:
            deleted = item.amount
            item.delete()
            return deleted
        else:
            item.amount -= amount
            item.save()
            return amount
    else:
        return -1


def add_item(name, storage_name='', storage_id='', amount=1, unit='', value='', worn=False):

    if storage_name != '':
        storage = models.Storage.objects.filter(name=storage_name)

    if storage_id != '':
        storage = models.Storage.objects.filter(pk=storage_id)

    if storage_id == '' and storage_name == '':
        return False

    item_type = models.ItemType.objects.filter(name=name)

    if not models.Item.objects.filter(stored=storage.pk).filter(item_type=item_type).exists():
        item = models.Item.objects.filter(stored=storage.pk).filter(item_type=item_type)
        item.amount += amount
        item.save()
        return True
    else:
        item = models.Item(type=item_type.pk, amount=amount, stored=storage.pk)
        if unit != '':
            item.unit = unit
        if value != '':
            item.value = value
        if worn:
            item.worn = True
        item.save()
        return True


def is_item(name, storage_name='', storage_id='', amount=0):
    if storage_name != '':
        storage = models.Storage.objects.filter(name=storage_name)

    if storage_id != '':
        storage = models.Storage.objects.filter(pk=storage_id)

    if storage_id == '' and storage_name == '':
        return False

    item_type = models.ItemType.objects.filter(name=name)

    if models.Item.objects.filter(stored=storage.pk).filter(item_type=item_type).exists():
        if models.Item.objects.filter(stored=storage.pk).filter(item_type=item_type).amount >= amount:
            return True
    return False



def update_food(character):
    pass  # Checks the character's rations set, deducts food from his food storage or inventory,
          # or adjusts ration setting if necessary


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
    now = datetime.date.today()
    start_date = models.Game.objects.get(id=0).start_date
    diff = start_date - now
    return diff.days + models.Game.objects.get(id=0).date_modifier


def get_skill(character, skill):
    try:
        char = models.Character.objects.get(name=character)
    except:
        return False
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
    if acre.farm:
        farm = models.Worksite.objects.filter(pk=acre.farm)
        employee = models.Employee.objects.filter(worksite=farm).filter(job=models.Job.objects.filter(name="farmer").pk)
        character = models.Character.objects.filter(pk=employee.character)
    elif acre.owner:
        character = models.Character.objects.filter(pk=acre.owner)
    else:
        character = None

    if models.Upgrade.objects.filter(acre=acre.pk).exists():
        for upgrade in models.Upgrade.objects.filter(acre=acre.pk):
            exec_script(os.path.join("acre", "upgrades"), upgrade.name, 'on_pre_update', acre)

    if acre.crop:
        crop = models.Crop.objects.filter(pk=acre.crop)
        if acre.temperature not in crop.temperature_survive:
            growth_time = (datetime.date.today() - acre.planted).days
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

            if not character or character.pk == acre.owner:
                last_30 = models.Tending.objects.filter(acre=acre.pk).filter(day__in=[get_current_day()-30, get_current_day()])
                if len(last_30) < 25:
                    acre.bonus -= 5
                    acre.save()

            if acre.growth_days == crop.time:
                acre.produce = crop.gross_yield * (1+(acre.bonus/100))
                if acre.fertility == "Barren":
                    acre.produce = int(acre.produce*0.1)
                elif acre.fertility == "Bad":
                    acre.produce = int(acre.produce*0.6)
                elif acre.fertility == "Fertile":
                    acre.produce = int(acre.produce*1.1)
                elif acre.fertility == "Very Fertile":
                    acre.produce = int(acre.prodce*1.3)
                acre.harvest_per = acre.produce / 5
                acre.save()
                if character:
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
                    if models.Tending.objects.filter(day=get_current_day()-count).filter(acre=acre.pk).exists and count <= 30:
                        acre.bonus += (models.Tending.objects.filter(day=get_current_day()-count).filter(acre=acre.pk).roll-crop.difficulty) * 5
                        running = False
                    elif count > 30:
                        running = False
                    else:
                        count += 1
                acre.save()
    if models.Upgrade.objects.filter(acre=acre.pk).exists():
        for upgrade in models.Upgrade.objects.filter(acre=acre.pk):
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
    f = os.path.join(os.path.abspath(__file__), 'scripts', path, name + ".py")
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