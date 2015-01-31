from django.apps import AppConfig
import neverwherebot.update as update

class NeverwhereAppConfig(AppConfig):
    name = "NeverwhereBot"
    verbose_name = "Neverwhere Bot"
    def ready(self):
        update.start()


