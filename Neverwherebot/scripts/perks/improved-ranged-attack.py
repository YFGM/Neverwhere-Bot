from Neverwherebot.perk import Perk
from Neverwherebot.models import Character


class Perk(Perk):
    name = "Improved Ranged Attack"
    description = "You are adept at ranged combat, giving you +1 to RAB."
    category = "Basic Tiered"

    def on_add(self, character):
        self.on_recalc(character)
        return True

    def on_recalc(self, character):
        try:
            char = Character.objects.get(name=character)
        except:
            return False
        char.rab += 1
        char.save()
        return True