import Neverwherebot.models as models
import Neverwherebot.update
import Neverwherebot.scripts.worksites.mine.miner as miner
import random

def update(character, employment, hour):
    random.seed()
    override = miner.check_upgrades("on_start", employment, character)

    if not employment.job.name == "overseer":
        print("Overseer.py update called without the employee being a farmer, what's up with that?")
        return False
    if hour in [11, 15] and employment.current_activity == "" and not override:
        override = miner.check_upgrades("on_overseer", employment, character)
        if not override:
            if employment.tunnel is not None:
                if not models.Overseeing.objects.filter(tunnel=employment.tunnel).filter(character=character).filter(day=Neverwherebot.update.get_current_day()).exists():
                    new = models.Overseeing()
                    new.character = character
                    new.tunnel = employment.tunnel
                    if employment.take_10:
                        new.roll = Neverwherebot.update.get_skill(character.name, "Mining") + 10
                    else:
                        new.roll = Neverwherebot.update.get_skill(character.name, "Mining") + random.randint(1, 20)
                    new.day = Neverwherebot.update.get_current_day()
                    new.save()
            else:
                message = "%s is currently not assigned to any tunnel, and is idle." % character.name
                Neverwherebot.update.send_message("", character.player.nick, message, flags="bwi")
            Neverwherebot.update.give_salary(character, employment.part, hour)
            return True

    if employment.current_activity != "":
        return miner.update(character, hour, employment)

    return True