from Neverwherebot.scripts.items.generics.item import Item
import Neverwherebot.models as models
from slugify import slugify

class Item(Item):
    wearable = True
    damage = ""
    ranged = False
    WEAPON_CLASSES = (
        "Simple",
        "Axes",
        "Bows",
        "Claw Weapons",
        "Crossbows",
        "Exotic Weapons",
        "Heavy Blades",
        "Light Blades",
        "Maces and Hammers",
        "Polearms",
        "Slings and Thrown Weapons",
        "Spears and Lances",
    )
    weapon_class = WEAPON_CLASSES[0]
    
    def on_recalc(self, character):
        try:
            char = models.Character.objects.get(name=character)
        except:
            print "Character not found."
            return False
        
        try:
            p = models.CharacterPerk.objects.filter(character=char).get(name="weapon-proficiency-"+slugify(self.weapon_class))
        except:
            if self.ranged:
                char.rab -= 4
                char.save()
            else :
                char.mab -= 4
                char.save()
        return True