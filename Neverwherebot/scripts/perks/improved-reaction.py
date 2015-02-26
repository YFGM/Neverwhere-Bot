from Neverwherebot.perk import Perk
from Neverwherebot.models import Character


class Perk(Perk):
    name = "Improved Reaction"
    description = "Your lightning reflexes increase your Re by 0.5."
    category = "Basic Tiered"

    def on_add(self, character):
        self.on_recalc(character)
        return True

    def on_recalc(self, character):
        try:
            char = Character.objects.get(name=character)
        except:
            return False
        char.re += 0.5
        char.save()
        return True