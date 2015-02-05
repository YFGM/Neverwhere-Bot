import Neverwherebot.models as models
import Neverwherebot.update
import random


def update(character, hour, employment):
    random.seed()
    if not models.Job.objects.filter(pk=employment.job).name == "farmer":
        print("Farmer.py update called without the employee being a farmer, what's up with that?")
        return False
    if hour == 15 and employment.current_activity == "":
        for acre in models.Acre.objects.filter(farm=employment.worksite):
            if not models.Tending.objects.filter(day=Neverwherebot.update.get_current_day()).filter(acre=acre).exists():
                roll = Neverwherebot.update.get_skill(character, "farming") + random.randint(1, 20)
                today = models.Tending(worksite=employment.worksite, day=Neverwherebot.update.get_current_day(), roll=roll, acre=acre)
                today.save()

    Neverwherebot.update.give_salary(character, employment.part, hour)
    return True


