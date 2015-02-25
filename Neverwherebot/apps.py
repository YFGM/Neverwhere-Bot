from django.apps import AppConfig
import Neverwherebot.update as update


class NeverwhereAppConfig(AppConfig):
    name = "Neverwherebot"
    verbose_name = "Neverwhere Bot"

    def ready(self):
        pass


