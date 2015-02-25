class Perk(object):

    name = ""
    description = ""
    category = ()

    def on_recalc(self, character):
        return True

    def on_add(self, character):
        return True

    def prerequisites(self, character):
        return True