# Utility class to make writing skill perks easier
from Neverwherebot.perk import Perk
import Neverwherebot.models as models


class Perk(Perk):
    category = ("Skill Tiered")

    def on_add(self, character):
        try:
            char = models.Character.objects.get(name=character)
        except:
            print "Character not found."
            return
        try:
            skill = models.Skill.objects.get(name=self.name)
        except:
            print "Skill not found."
            return
        if not models.CharacterSkill.objects.filter(skill=skill).filter(character=char).exists:
            print "Char skill not present, creating."
            new = models.CharacterSkill()
            new.skill = skill
            new.character = char
            new.save()
            print "Char skill created."
            return True

    def on_recalc(self, character):
        try:
            char = models.Character.objects.get(name=character)
        except:
            print "Character not found."
            return

        try:
            skill = models.Skill.objects.get(name=self.name)
        except:
            print "Skill not found."
            return

        try:
            charskill = models.CharacterSkill.objects.filter(skill=skill).get(character=char)
        except:
            print "Charskill not found."
            return
        if charskill.level == 0 or charskill.level == 2:
            charskill.level += 2
        else:
            charskill.level += 1

        charskill.save()
        return True