import Neverwherebot.models as models
import Neverwherebot.update
import random
import os


def update(character, hour, employment):
    random.seed()
    override = check_upgrades("on_start", employment, character)

    if not models.Job.objects.filter(pk=employment.job).name == "farmer":
        print("Farmer.py update called without the employee being a farmer, what's up with that?")
        return False
    if hour == 15 and employment.current_activity == "" and not override:
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
                            message = "Today, you harvested %ikg of &s from acre %s, harvesting the acre completely." % (
                                acre.produce, crop.product_name, acre.id
                            )
                            acre.produce = 0
                            acre.tilled = 0
                            acre.crop = None
                            acre.harvest_per = 0
                            acre.planted = None
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
                                    acre.produce = 0
                                    acre.tilled = 0
                                    acre.crop = None
                                    acre.harvest_per = 0
                                    acre.planted = None
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


def check_upgrades(function, employment, *args):
    if models.Upgrade.objects.filter(worksite=employment.worksite).exists():
        for upgrade in models.Upgrade.objects.filter(worksite=employment.worksite):
            result = Neverwherebot.update.exec_script(os.path.join("worksites", "farm", "upgrades"), upgrade.name, function, *args)
            if result == "override":
                return True
            else:
                return False