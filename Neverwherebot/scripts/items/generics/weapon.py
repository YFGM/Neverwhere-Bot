from Neverwherebot.scripts.items.generics.item import Item
import Neverwherebot.models as models

class Item(Item):
    wearable = True
    damage = ""
    ranged = False
    WEAPON_CLASSES = (
        ('S', "Simple"),
        ('A', "Axes"),
        ('B', "Bows"),
        ('CW', "Claw Weapons"),
        ('C', "Crossbows"),
        ('EW', "Exotic Weapons"),
        ('HB', "Heavy Blades"),
        ('LB', "Light Blades"),
        ('M', "Maces and Hammers"),
        ('P', "Polearms"),
        ('ST', "Slings and Thrown Weapons"),
        ('SP', "Speaks and Lances"),
    )
    weapon_class = ""
    
    def on_recalc(self, character):
        try:
            char = models.Character.objects.get(name=character)
        except:
            print "Character not found."
            return False
        
        try:
            p = models.CharacterPerk.objects.filter(character=char).get(slug="weapon-profficiency-"+self.weapon_class)
        except:
            if self.ranged:
                char.rab -= 4
                char.save()
            else :
                char.mab -= 4
                char.save()
        return True