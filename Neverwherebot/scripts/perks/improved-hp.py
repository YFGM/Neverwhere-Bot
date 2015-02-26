from Neverwherebot.perk import Perk
from Neverwherebot.models import Character


class Perk(Perk):
    name = "Improved HP"
    description = "You are unusually hardy, you gain +2 HP."
    category = ("Basic", "Tiered")

    def on_add(self, character):
        self.on_recalc(character)
        return True

    def on_recalc(self, character):
        char = Character.objects.filter(name=character)
        if not char:
            return False
        char.hp += 2
        char.save()
        return True