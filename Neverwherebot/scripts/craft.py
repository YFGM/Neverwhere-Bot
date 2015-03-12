import Neverwherebot.update as update
import Neverwherebot.models as models
import os
import random
import math

def update(character, employment, hour):
    random.seed()
    override = False
    if not "craft" in employment.current_activity:
        return False
        
    if employment.craft is None:
        return False
    
    if employment.worksite is not None:
        override = check_upgrades("on_pre_craft", employment)
        
    if hour in range(8, 16) and not override:
        override = check_upgrades("on_craft", employment)
        if not override:
            if employment.craft.skill is None:
                skill = employment.craft.attribute
            else:
                skill = employment.craft.skill.name
            if employment.take_10:
                roll = update.get_skill(character.name, skill) + 10
            else:
                roll = random.randint(1, 20)
                if roll == 1:
                    # Critical fail
                    pass
                if roll == 20:
                    # Critical success
                    pass
                roll += update.get_skill(character.name, skill)
            
            if employment.craft.difficulty == "Simple":
                difficulty = 5.0
            elif employment.craft.difficulty == "Average":
                difficulty = 10.0
            elif employment.craft.difficulty == "Complex":
                difficulty = 15.0
            else:
                difficulty = 20.0
            
            result = int(math.floor(roll / difficulty))
            
            hours = int(math.ceil(employment.craft.item.value / 3.0 * employment.craft.item.wr / 2)) # 2 is hour value
            
            if employment.craft.hours + result >= hours:
                if employment.craft.worksite is None and employment.worksite is None:
                    s = update.add_item(employment.craft.item.name, storage_id=employment.character.inventory.pk)
                    if isinstance(s, basestring):
                        #Panic
                        if s == "Not enough room left in the storage.":
                            message = "You finished crafting %s, but your inventory was full and you couldn't carry it." \
                            " Your crafting has been set on hold. Free enough space in your inventory and claim your item using: " \
                            "!craft claim %i" % (employment.craft.item.name, employment.craft.pk)
                            update.send_message("", employment.character.player.nick, message, flags="bwi")
                            employment.current_activity = ""
                            employment.save()
                            employment.craft.hours += result
                            employment.craft.save()
                            update.give_salary(character, employment.part, hour)
                            return True
                        return False
                    employment.craft.amount -= 1
                    employment.craft.save()
                    message = "You finished crafting 1 %s." % employment.craft.item.name
                    update.send_message("", employment.character.player.nick, message, flags="bw")
                    if employment.craft.amount <= 0:
                        employment.craft.delete()
                        employment.current_activity = ""
                        employment.save()
                        ac = update.get_next_unbound(character)
                        if ac.employment == employment or ac.employment is None:
                            update.apply_activity(ac)
                    return True
                        
                elif employment.craft.worksite is not None:
                    s = update.add_item(employment.craft.item.name, storage_id=employment.craft.worksite.storage.pk)
                    if isinstance(s, basestring):
                        if s == "Not enough room left in the storage.":
                            message = "You finished crafting %s, but your worksite's storage was full and you couldn't store it." \
                            " Your crafting has been set on hold. Free enough space in your storage and claim your item using: " \
                            "!craft claim %i" % (employment.craft.item.name, employment.craft.pk)
                            update.send_message("", employment.character.player.nick, message, flags="bwi")
                            employment.current_activity = ""
                            employment.save()
                            employment.craft.hours += result
                            employment.craft.save()
                            update.give_salary(character, employment.part, hour)
                            return True
                        return False
                    employment.craft.amount -= 1
                    employment.craft.save()
                    message = "You finished crafting 1 %s." % employment.craft.item.name
                    update.send_message("", employment.character.player.nick, message, flags="bw")
                    if employment.craft.amount <= 0:
                        employment.craft.delete()
                        employment.current_activity = ""
                        employment.save()
                        ac = update.get_next_unbound(character)
                        if ac.employment == employment or ac.employment is None:
                            update.apply_activity(ac)
                    update.give_salary(character, employment.part, hour)
                    return True
                elif employment.worksite is not None:
                    s = update.add_item(employment.craft.item.name, storage_id=employment.worksite.storage.pk)
                    if isinstance(s, basestring):
                        if s == "Not enough room left in the storage.":
                            message = "You finished crafting %s, but your worksite's storage was full and you couldn't store it." \
                            " Your crafting has been set on hold. Free enough space in your storage and claim your item using: " \
                            "!craft claim %i" % (employment.craft.item.name, employment.craft.pk)
                            update.send_message("", employment.character.player.nick, message, flags="bwi")
                            employment.current_activity = ""
                            employment.save()
                            employment.craft.hours += result
                            employment.craft.save()
                            update.give_salary(character, employment.part, hour)
                            return True
                        return False
                    employment.craft.amount -= 1
                    employment.craft.save()
                    message = "You finished crafting 1 %s." % employment.craft.item.name
                    update.send_message("", employment.character.player.nick, message, flags="bw")
                    if employment.craft.amount <= 0:
                        employment.craft.delete()
                        employment.current_activity = ""
                        employment.save()
                        ac = update.get_next_unbound(character)
                        if ac.employment == employment or ac.employment is None:
                            update.apply_activity(ac)
                    update.give_salary(character, employment.part, hour)
                    return True
            else:
                employment.craft.hours += result
                employment.craft.save()
                if hour == 15:
                    message = "You spent most of today working on crafting %s, but have yet to finish" % employment.craft.item.name
                update.give_salary(character, employment.part, hour)
                return True
        
        
        
        
        
        
        
def check_upgrades(function, employment, *args):
    if models.Upgrade.objects.filter(worksite=employment.worksite).exists():
        for upgrade in models.Upgrade.objects.filter(worksite=employment.worksite):
            result = update.exec_script(os.path.join("worksites", employment.worksite.type, "upgrades"), upgrade.type.name, function, *args)
            if result == "override":
                return True
            else:
                return False 