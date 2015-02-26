from Neverwherebot.perk import Perk
from Neverwherebot.models import Character


class Perk(Perk):
    name = "Improved FP"
    description = "You have great stamina, increasing your FP by +1."
    category = "Basic Tiered"

    def on_add(self, character):
        self.on_recalc(character)
        return True

    def on_recalc(self, character):
        try:
            char = Character.objects.get(name=character)
        except:
            return False
        char.fp += 1
        char.save()
        return True