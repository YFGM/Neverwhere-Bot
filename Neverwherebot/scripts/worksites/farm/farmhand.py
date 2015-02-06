import Neverwherebot.models as models
import Neverwherebot.update
import Neverwherebot.scripts.worksites.farm.farmer as farmer


def update(character, hour, employment):
    if not models.Job.objects.filter(pk=employment.job).name == "farmhand":
        print("Farmhand.py update called without the employee being a farmer, what's up with that?")
        return False
    if hour == 15 and employment.current_activity == "":
        Neverwherebot.update.give_salary(character, employment.part, hour)
        return True
