# Utility class to make writing skill perks easier
from Neverwherebot.perk import Perk
import Neverwherebot.models as models


class Perk(Perk):
    category = ("Skill Tiered")

    def on_add(self, character):
        char = models.Character.objects.get(name=character)
        skill = models.Skill.objects.get(name=self.name)
        if not models.CharacterSkill.objects.filter(skill=skill).filter(character=char).exists:
            new = models.CharacterSkill()
            new.skill = skill
            new.character = char
            new.save()
            return True

    def on_recalc(self, character):
        try:
            char = models.Character.objects.get(name=character)
        except:
            print "Character not found."

        try:
            skill = models.Skill.objects.get(name=self.name)
        except:
            print "Skill not found."

        try:
            charskill = models.CharacterSkill.objects.filter(skill=skill).get(character=char)
        except:
            print "Charskill not found."
        if charskill.level == 0 or charskill.level == 2:
            charskill.level += 2
        else:
            charskill.level += 1

        charskill.save()
        return True