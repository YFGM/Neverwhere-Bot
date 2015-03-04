import Neverwherebot.models as models
import Neverwherebot.update
import Neverwherebot.scripts.worksites.farm.farmer as farmer


def update(character, hour, employment):
    override = farmer.check_upgrades("on_start", employment, character)

    if not employment.job.name == "farmhand":
        print("Farmhand.py update called without the employee being a farmer, what's up with that?")
        return False
    if hour == 15 and employment.current_activity == "" and not override:
        override = farmer.check_upgrades("on_farmhand", employment, character)
        if not override:
            Neverwherebot.update.give_salary(character, employment.part, hour)
            return True

    if employment.current_activity != "":
        return farmer.update(character, hour, employment)

    return True