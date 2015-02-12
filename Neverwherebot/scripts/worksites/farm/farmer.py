import Neverwherebot.models as models
import Neverwherebot.update
import random
import os
import datetime


def update(character, hour, employment):
    random.seed()
    override = check_upgrades("on_start", employment, character)

    if hour == 15 and employment.current_activity == "" and not override:
        if not models.Job.objects.filter(pk=employment.job).name == "farmer":
            print("Farmer.py update called without the employee being a farmer, what's up with that?")
            return False
        override = check_upgrades("on_farm", employment, character)
        if not override:
            for acre in models.Acre.objects.filter(farm=employment.worksite):
                if not models.Tending.objects.filter(day=Neverwherebot.update.get_current_day()).filter(acre=acre).exists():
                    roll = Neverwherebot.update.get_skill(character, "farming") + random.randint(1, 20)
                    today = models.Tending(worksite=employment.worksite, day=Neverwherebot.update.get_current_day(), roll=roll, acre=acre)
                    today.save()
                    check_upgrades("on_tend", employment, character, today)

        Neverwherebot.update.give_salary(character, employment.part, hour)
        return True

    if hour in range(8, 16) and "tilling" in employment.current_activity and not override:
        override = check_upgrades("on_till", employment, character)
        done = False
        if not override:
            if employment.acre:
                acre = models.Acre.objects.filter(pk=employment.acre)
                if acre.tilled < 20:
                    if hour == 15:
                        acre.tilled += 1
                        acre.save()
                        message = "Today, you worked on tilling acre %s, but you think around %i more man-days are necessary." % (
                            acre.id, 20 - acre.tilling
                        )
                        done = True
                    if acre.tilled == 20:
                        message = "You finished tilling acre %s" % acre.id
                else:
                    if employment.current_activity == "tilling_all":
                        found = False
                        for a in models.Acre.objects.filter(worksite=employment.worksite):
                            if a.tilled < 20:
                                employment.acre = a.pk
                                employment.save()
                                found = True
                                message = "Having finished tilling the last, you have moved on to work on acre " \
                                          "%s." % acre.id
                                if not done:
                                    a.tilled += 1
                                    a.save()
                                break
                        if not found:
                            message = "Having nothing to till, you have been set back to idle activity."
                            employment.acre = None
                            employment.current_activity = ""
                            employment.save()
                    else:
                        message = "You have finished tilling acre %s, and have now been set to idle work. " % acre.id
                        employment.current_activity = ""
                        employment.acre = None
                        employment.save()
            else:
                if employment.current_activity == "tilling_all":
                        for a in models.Acre.objects.filter(worksite=employment.worksite):
                            if a.tilled < 20:
                                employment.acre = a.pk
                                employment.save()
                                message = "Having finished tilling the last, you have moved on to work on acre " \
                                          "%s." % a.id
                                if not done:
                                    a.tilled += 1
                                    a.save()
                                break
                else:
                    message = "Having nothing to till, you have been set back to idle activity."
                    employment.current_activity = ""
                    employment.save()
            Neverwherebot.update.send_message("", character.name, message, "bw")
            Neverwherebot.update.give_salary(character, employment.part, hour)
            return True

    if hour in range(8, 16) and "harvesting" in employment.current_activity and not override:
        override = check_upgrades("on_harvest", employment, character)
        if not override:
            done = False
            if employment.acre:
                acre = models.Acre.objects.filter(pk=employment.acre)
                crop = models.Crop.objects.filter(pk=acre.crop)
                worksite = models.Worksite.objects.filter(pk=employment.worksite)
                if acre.produce > 0:
                    if hour == 15:
                        if acre.produce - acre.harvest_per >= 0:
                            Neverwherebot.update.add_item(crop.product_name, storage_id=worksite.storage, amount=acre.harvest_per)
                            acre.produce -= acre.harvest_per
                            acre.save()
                            message = "Today, you harvested %ikg of %s from acre %s, leaving roughly %ikg for harvesting" % (
                                acre.harvest_per, crop.product_name, acre.id, acre.produce
                            )
                            done = True
                        else:
                            Neverwherebot.update.add_item(crop.product_name, storage_id=worksite.storage, amount=acre.produce)
                            message = "Today, you harvested %ikg of %s from acre %s, harvesting the acre completely." % (
                                acre.produce, crop.product_name, acre.id
                            )
                            if not crop.perennial:
                                acre.produce = 0
                                acre.tilled = 0
                                acre.crop = None
                                acre.harvest_per = 0
                                acre.planted = None
                                acre.bonus = 0
                                acre.growth_days = 0
                                acre.save()
                            else:
                                acre.produce = 0
                                acre.tilled = 0
                                acre.harvest_per = 0
                                acre.bonus = 0
                                acre.growth_days = 0
                                acre.save()
                            employment.acre = None
                            employment.save()
                            done = True
                if acre.produce == 0 or not employment.acre:
                    if employment.current_activity == "harvesting_all":
                        for a in models.Acre.objects.filter(worksite=worksite.pk):
                            if a.produce > 0:
                                employment.acre = a.pk
                                employment.save()
                                break
                        if models.Acre.objects.filter(pk=employment.acre).produce > 0 and not done:
                            if hour == 15:
                                if acre.produce - acre.harvest_per >= 0:
                                    Neverwherebot.update.add_item(crop.product_name, storage_id=worksite.storage, amount=acre.harvest_per)
                                    acre.produce -= acre.harvest_per
                                    acre.save()
                                    message = "Today, you harvested %ikg of %s from acre %s, leaving roughly %ikg for harvesting" % (
                                        acre.harvest_per, crop.product_name, acre.id, acre.produce
                                    )
                                    done = True
                                else:
                                    Neverwherebot.update.add_item(crop.product_name, storage_id=worksite.storage, amount=acre.produce)
                                    message = "Today, you harvested %ikg of %s from acre %s, harvesting the acre completely." % (
                                        acre.produce, crop.product_name, acre.id
                                    )
                                    if not crop.perennial:
                                        acre.produce = 0
                                        acre.tilled = 0
                                        acre.crop = None
                                        acre.harvest_per = 0
                                        acre.planted = None
                                        acre.bonus = 0
                                        acre.growth_days = 0
                                        acre.planting = 0
                                        acre.save()
                                    else:
                                        acre.produce = 0
                                        acre.harvest_per = 0
                                        acre.bonus = 0
                                        acre.growth_days = 0
                                        acre.save()
                                    employment.acre = None
                                    employment.save()
                                    done = True
                        elif models.Acre.objects.filter(pk=employment.acre).produce == 0:
                            message += "You were unable to find any further acres to harvest today, and have been set back to idle."
                            employment.current_activity = ""
                            employment.acre = None
                            employment.save()
                    elif employment.current_activity == "harvesting":
                        message += "You have finished harvesting acre %s and have been set back to idle." % acre.id
                        employment.current_activity = ""
                        employment.acre = None
                        employment.save()
            Neverwherebot.update.give_salary(character, employment.part, hour)
            return True

    if hour in range(8, 16) and "planting" in employment.current_activity and not override:
        override = check_upgrades("on_plant", employment, character)
        if not override:
            done = False
            if employment.acre:
                acre = models.Acre.objects.filter(pk=employment.acre)
                worksite = models.Worksite.objects.filter(pk=employment.worksite)
                if acre.planting < 8:
                    if acre.planting == 0:
                        start_planting(employment)
                        done = True
                    else:
                        acre.planting += 1
                        acre.save()
                        done = True
                    if hour == 15 and acre.planting < 8:
                        message = "You spent most of today planting %s on acre %s, but have yet to finish." % (
                            models.Crop.objects.filter(pk=acre.crop), acre.id
                        )
                    elif hour == 15:
                        message = "Today, you finished planting %s on acre %s." % (
                            models.Crop.objects.filter(pk=acre.crop), acre.id
                        )
                        acre.planted = datetime.datetime.now()
                        acre.save()

                if not acre.planting < 8:
                    message2 = "You finished planting acre %s." % acre.id

                if "planting_all" in employment.current_activity and not acre.planting < 8:
                    for a in models.Acre.objects.filter(worksite=worksite.pk):
                        if a.planting < 8:
                            employment.acre = a.pk
                            employment.save()
                            break
                    if models.Acre.objects.filter(pk=employment.acre).planting < 8 and not done:
                        failed = False
                        if acre.planting == 0:
                            if start_planting(employment):
                                message2 = "You began planting on acre %s." % acre.id
                            else:
                                message2 = "You wanted to start planting on acre %s, but could not find " \
                                            "sufficient seed to do so and have been set to idle." % acre.id
                                employment.current_activity = ""
                                employment.acre = None
                                employment.save()
                                failed = True
                        else:
                            acre.planting += 1
                            acre.save()
                        if hour == 15 and acre.planting < 8 and not failed:
                            message = "You spent most of today planting %s on acre %s, but have yet to finish." % (
                                models.Crop.objects.filter(pk=acre.crop), acre.id
                            )
                        elif hour == 15 and not failed:
                            message = "Today, you finished planting %s on acre %s." % (
                                models.Crop.objects.filter(pk=acre.crop), acre.id
                            )
                            acre.planted = datetime.datetime.now()
                            acre.save()
                        if not acre.planting < 8 and not failed:
                            message2 = "You finished planting acre %s." % acre.id
                            acre.planted = datetime.datetime.now()
                            acre.save()
                    elif models.Acre.objects.filter(pk=employment.acre).planting == 8:
                        message = "Having finished planting acre %s, you could find no other acres to plant on, and" \
                                  " have been set back to idle." % acre.id
                        employment.current_activity = ""
                        employment.acre = None
                        employment.save()
                elif not acre.planting < 8:
                    message = "Having finished planting acre %s, you could find no other acres to plant on, and" \
                                  " have been set back to idle." % acre.id
                    employment.current_activity = ""
                    employment.acre = None
                    employment.save()
            else:
                message = "Having finished planting the previous acre, you could find no other acres to plant on, and" \
                                  " have been set back to idle."
                employment.current_activity = ""
                employment.acre = None
                employment.save()

            Neverwherebot.update.send_message("", character.name, message, "bw")
            if message2 in locals():
                Neverwherebot.update.send_message("", character.name, message2, "bw")
            Neverwherebot.update.give_salary(character, employment.part, hour)
            return True
    if hour in range(8, 16) and "burning" in employment.current_activity and not override:
        override = check_upgrades("on_burn", employment)
        if not override:
            if not employment.acre:  # Shouldn't happen
                employment.current_activity = ""
                employment.save()
                return False
            else:
                acre = models.Acre.objects.filter(pk=employment.acre)
                if acre.crop is not None:
                    acre.reset()
                    if acre.fertility == "Barren":
                        acre.fertility = "Bad"
                        acre.save()
                    elif acre.fertility == "Bad":
                        acre.fertility = "Normal"
                        acre.save()
                    message = "You burnt the acre %s to the ground." % acre.id
                    employment.current_activity = ""
                    employment.acre = None
                    employment.save()
                else:
                    message = "You wanted to burn the care %s, but there was nothing there worth burning." % acre.id
                    employment.current_activity = ""
                    employment.acre = None
                    employment.save()
            Neverwherebot.update.send_message("", character.name, message, "bw")
            Neverwherebot.update.give_salary(character, employment.part, hour)
            return True

    else:
        return True


def check_upgrades(function, employment, *args):
    if models.Upgrade.objects.filter(worksite=employment.worksite).exists():
        for upgrade in models.Upgrade.objects.filter(worksite=employment.worksite):
            result = Neverwherebot.update.exec_script(os.path.join("worksites", "farm", "upgrades"), upgrade.name, function, *args)
            if result == "override":
                return True
            else:
                return False


def start_planting(employment):
    character = models.Character.objects.filter(pk=employment.character)
    acre = models.Acre.objects.filter(pk=employment.acre)
    crop_name = employment.current_activity[13:]  # Strip away "planting_all "
    crop = models.Crop.objects.filter(name=crop_name)
    seed = models.ItemType.objects.filter(pk=crop.seed_type)
    worksite = models.Worksite.objects.filter(pk=employment.worksite)
    storage = models.Storage.objects.filter(pk=worksite.storage)
    if Neverwherebot.update.is_item(seed.name, storage_id=storage.id, amount=crop.seed):
        Neverwherebot.update.remove_item(seed.name, storage_id=storage.id, amount=crop.seed)
        acre.crop = crop.pk
        acre.planting = 1
        acre.planted = datetime.datetime.now()
        acre.save()
        return True

    elif Neverwherebot.update.is_item(seed.name, storage_id=character.inventory, amount=crop.seed):
        Neverwherebot.update.remove_item(seed.name, storage_id=character.inventory, amount=crop.seed)
        acre.crop = crop.pk
        acre.planting = 1
        acre.save()
        return False
