import os
import threading
import imp
import datetime

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

        if update_jobs(character, scripts, scripts_dir, hour, day):
            count += 1
        else:
            failed_count += 1
            failed = failed + (character.name + ": " + character.job.name)

    print("Succesfully updated %s character jobs, %s failed, namely: %s" % (str(count), str(failed_count), str(failed)))

    if hour == 12:
        update_food(character)

    if is_winter():
        check_for_freezing(character, hour)

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
    pass  # Return a list of all character objects by querying models or SQL?


def get_acres():
    pass  # Returns a list of all acre objects by querying models or SQL?


def get_storages():
    pass  # Returns a list of all storage objects by querying models or SQL?


def get_cyclical_items():
    pass  # Returns a list of all items that have the "Cyclical Effect" flag


def update_recovery(character, hour):
    pass  # Checks whether the character is valid to recover HP or similar and does so if yes.


def update_jobs(character, scripts, scripts_dir, hour, day):
    jobs = character.get_jobs()
    for job in jobs:
        if job.part == 1 and hour in range(8, 11) or job.part == 2 and hour in range(12, 15) or job.part == 0 and hour in range (8, 15):
            worksite = job.get_worksite()
            if not worksite.name:
                if job.name == "craft":
                    try:
                        mod = imp.load_source("craft", os.path.join(scripts_dir, "craft.py"))
                    except:
                        print("Failed to load crafting script! This isn't good.")
                        return False
                    try:
                        mod.update(character, job, hour, day)
                    except:
                        print("Failed to execute update in craft.py!")
                        return False
            elif os.path.join(scripts_dir, worksite.name) in scripts:
                job_script = job.name + ".py"
                if job_script in scripts[os.path.join(scripts_dir, worksite.name)]:
                    try:
                        mod = imp.load_source(job_script[:-3], os.path.join(scripts_dir, worksite.name, job_script))
                    except:
                        print("Failed to load job script %s, even so it should exist.", job_script)
                        return False

                    try:
                        mod.update(character, hour, day)
                    except:
                            print("Failed to execute update method in %s", job_script)
                            return False
                else:
                    print("Couldn't find script for %s, assuming it is a service job", job.name)
                    give_salary(character, job.part, hour, day)
    return True


def give_salary(character, part, hour, day):
    pass  # Checks the character's job (if part time, one or two) and checks SQL for what salary is owned if any,
          # and gives such


def update_food(character):
    pass  # Checks the character's rations set, deducts food from his food storage or inventory,
          # or adjusts ration setting if necessary


def is_winter():
    pass  # Returns whether it is currently winter or not


def check_for_freezing(character, hour):
    pass  # Check severity of winter setting, modify by hour of day, check character housing, apply freezing problems

