from Neverwherebot.scripts.items.generics.item import Item
import Neverwherebot.models as models
from slugify import slugify

class Item(Item):
    wearable = True
    category = ""
    ac = 0
    ap = 0
    md = 0
    
    def on_recalc(self, character):
        try:
            char = models.Character.objects.get(name=character)
        except:
            print "Character not found."
            return False
        if char.re > self.md:
            char.ac -= char.re - self.md
            char.save()
        
        for s in models.CharacterSkill.objects.filter(character=char).filter(skill__in=models.Skill.objects.filter(attribute__in="Strength Dexterity")):
            s -= self.ap
            s.save()
            
        try:
            p = models.CharacterPerk.objects.filter(character=char).get(name="armor-proficiency-"+slugify(self.category))
        except:
            char.mab -= self.ap
            char.rab -= self.ap
            char.save()
        char.ac += self.ac
        char.save()
        return True