import os
import threading
import imp
import datetime
import math
import neverwherebot.models as models

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
        acre.update(hour, day)  # Set growth and such

    for storage in storages:
        storage.update(hour, day)  # Check for spoilage etc

    for item in cyclic_items:
        item.on_cycle(scripts, hour, day)


def enumerate_scripts(scripts_dir):
    # Returns a directory with the directory's path name as key leading to a tuple of scripts
    scripts = {}
    for dirname, dirnames, filenames in os.walk(dir):
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
            if not worksite.name:
                if job.type == "craft":
                    try:
                        mod = imp.load_source("craft", os.path.join(scripts_dir, "craft.py"))
                    except:
                        print("Failed to load crafting script! This isn't good.")
                        return False
                    try:
                        mod.update(character, job, hour)
                    except:
                        print("Failed to execute update in craft.py!")
                        return False
                else:
                    print("No worksite found for character %s job %s." % (character.name, str(job.part)))
                    return False
            elif os.path.join(scripts_dir, worksite.type) in scripts:
                job_script = job.name + ".py"
                if job_script in scripts[os.path.join(scripts_dir, worksite.type)]:
                    try:
                        mod = imp.load_source(job_script[:-3], os.path.join(scripts_dir, worksite.name, job_script))
                    except:
                        print("Failed to load job script %s, even so it should exist." % job_script)
                        return False
                    try:
                        mod.update(character, hour, day)
                    except:
                            print("Failed to execute update method in %s" % job_script)
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
                str(datetime.datetime.now()), charactern.name, str(money), worksite.name,
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
    if sender != '':
        s = models.Player.objects.filter(nick=sender)
    else:
        s = models.Player.objects.get(pk=1)

    r = models.Player.objects.filter(nick=receiver)

    if len(content) >= 10000:
        return False

    if r.exists():
        m = models.Message(sender=s.nick, receiver=r.nick, message=content, flags=flags)
        m.save()


def get_current_day():
    now = datetime.date.today()
    start_date = models.Game.objects.get(pk=1).start_date
    diff = start_date - now
    return diff.days