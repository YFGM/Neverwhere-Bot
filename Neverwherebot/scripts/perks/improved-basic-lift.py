import Neverwherebot.perk
from Neverwherebot.models import Character, CharacterPerk, Perk
from slugify import slugify

class Perk(Neverwherebot.perk.Perk):
    name = "Improved Basic Lift"
    description = "Your senses are especially canny, giving you +1 to Per."
    category = "Basic Tiered"

    def on_add(self, character):
        self.on_recalc(character)
        return True

    def on_recalc(self, character):
        try:
            char = Character.objects.get(name=character)
        except:
            return False
        char.bl += char.str**2 / 100
        char.save()
        return True

    def prerequisites(self, character):
        char = Character.objects.get(name=character)
        p = Perk.objects.get(name=slugify(self.name))
        count = 0
        for cp in CharacterPerk.objects.filter(character=char):
            if cp.perk == p:
                count += 1
        if count >= 10:
            return False
        else:
            return True