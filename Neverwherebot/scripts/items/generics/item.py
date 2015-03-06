import Neverwherebot.models as models

class Item(object):
    name = ""
    wearable = False
    el = 0
    kcal = 0

    def on_equip(self, character):
        if not self.wearable:
            return False
        if not self.check_equip(character):
            return False
        return self.on_recalc(character)
    
    def on_recalc(self, character):
        return True
    
    def on_cycle(self, storage):
        return True
    
    def on_attack(self, character):
        return True
    
    def check_equip(self, character):
        try:
            char = models.Character.objects.get(name=character)
        except:
            print "Character not found."
            return False
        
        try:
            s = models.ItemType.objects.get(name=self.name)
        except:
            print "Cannot find self."
            return False
        
        items = models.Item.objects.filter(worn=True).filter(storage=char.inv)
        for i in items:
            if i.type.slot == s.slot:
                return False
        return True