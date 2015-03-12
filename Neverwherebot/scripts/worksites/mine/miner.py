import Neverwherebot.models as models
import Neverwherebot.update as update
import os


def update(character, employment, hour):
    override = check_upgrades("on_start", employment, character)
    if hour in range(8, 16) and employment.current_activity == "" and not override:
        done = False
        if not employment.job.name == "miner":
            print("Miner.py update called without the employee being a miner, what's up with that?")
            return False
        override = check_upgrades("on_mine", employment, character)
        if not override:
            if employment.worksite.depth_dug < models.MiningSite.objects.get(worksite=employment.worksite).depth:
                employment.current_activity = "digging"
                employment.save()
                done = False
            else:
                if employment.tunnel is not None:
                    bonus = 0.0
                    for o in models.Overseeing.objects.filter(day=update.get_current_day-1):
                        bonus += (o.roll - 10) * 0.05
                    if employment.tunnel.richness == "Dead":
                        employment.tunnel = None
                        employment.save()
                        message = "The tunnel %s was working in has run dry, and they have been set back to idle." % character.name
                        update.send_message("", character.player.nick, message, flags="bwi")
                        value = 0.0
                    if employment.tunnel.richness == "Barren":
                        value = 0.1 * (1 + bonus)
                    if employment.tunnel.richness == "Normal":
                        value = 1.0 * (1 + bonus)
                    if employment.tunnel.richness == "Rich":
                        value = 10.0 * (1 + bonus)
                    if employment.tunnel.richness == "Bountiful":
                        value = 50.0 * (1 + bonus)
                    amount = value / employment.tunnel.ore.value
                    update.add_item(employment.tunnel.ore.name, storage_id=employment.worksite.storage.pk, amount=amount)
                    done = True
                else:
                    message = "%s is not set to any tunnel to work in, and is being idle." % character.name
                    update.send_message("", character.player.nick, message, flags="bwi")
                    update.give_salary(character, employment.part, hour)
                    return True
        if done:
            update.give_salary(character, employment.part, hour)
            return True
        
    elif hour in range(8, 16) and employment.current_activity == "digging" and not override:
        try:
            u = models.Item.objects.filter(stored=employment.worksite.storage).get(type__in=models.ItemType.objects.filter(name__contains="Mineshaft"))
            if update.remove_item(u.type.name, storage_id=employment.worksite.storage) == 1.0:
                new = models.Upgrade()
                new.worksite = employment.worksite
                new.type = models.UpgradeType.objects.get(name="Mineshaft")
                new.save()
                update.exec_script(os.path.join("worksites", "mine", "upgrades"), "Mineshaft", "on_install", employment.worksite)
            else:
                return False
        except:
            pass
        try:
            c = models.Craft.objects.filter(character=employment.worksite.owner).filter(worksite=employment.worksite).get(item__in=models.ItemType.objects.filter(name__contains="Mineshaft"))
            employment.craft = c
            employment.current_activity = "crafting"
            ret = update.exec_script("", "craft", "update", character, employment, hour)
            try:
                u = models.Item.objects.filter(stored=employment.worksite.storage).get(type__in=models.ItemType.objects.filter(name__contains="Mineshaft"))
                if update.remove_item(u.type.name, storage_id=employment.worksite.storage) == 1.0:
                    new = models.Upgrade()
                    new.worksite = employment.worksite
                    new.type = models.UpgradeType.objects.get(name="Mineshaft")
                    new.save()
                    update.exec_script(os.path.join("worksites", "mine", "upgrades"), "Mineshaft", "on_install", employment.worksite)
                    return ret
                else:
                    return False
            except:
                return ret
                
        except:
            if employment.worksite.depth_dug < models.MiningSite.objects.get(worksite=employment.worksite).depth:
                craft = models.Craft()
                craft.item = models.ItemType.objects.get(name="Mineshaft")
                craft.character = employment.worksite.owner
                craft.skill = None
                craft.attribute = "str"
                craft.worksite = employment.worksite
                craft.difficulty = "Simple"
                craft.started = update.get_current_day()
                craft.coop = 100
                craft.save()
                employment.current_activity = "crafting"
                employment.craft = craft
                employment.save()
                ret = update.exec_script("", "craft", "update", character, employment, hour)
                try:
                    u = models.Item.objects.filter(stored=employment.worksite.storage).get(type__in=models.ItemType.objects.filter(name__contains="Mineshaft"))
                    if update.remove_item(u.type.name, storage_id=employment.worksite.storage) == 1.0:
                        new = models.Upgrade()
                        new.worksite = employment.worksite
                        new.type = models.UpgradeType.objects.get(name="Mineshaft")
                        new.save()
                        update.exec_script(os.path.join("worksites", "mine", "upgrades"), "Mineshaft", "on_install", employment.worksite)
                        return ret
                    else:
                        return False
                except:
                    return ret
            else:
                message = "%s has no mineshafts left to dig, and has been set to idle." % character.name
                update.send_message("", character.player.nick, message, flags="bwi")
                employment.current_activity = ""
                employment.save()
    
    
def check_upgrades(function, employment, *args):
    if models.Upgrade.objects.filter(worksite=employment.worksite).exists():
        for upgrade in models.Upgrade.objects.filter(worksite=employment.worksite):
            result = update.exec_script(os.path.join("worksites", "mine", "upgrades"), upgrade.type.name, function, *args)
            if result == "override":
                return True
            else:
                return False
    return False