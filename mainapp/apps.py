from django.apps import AppConfig


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'mainapp'

    def ready(self):
        import mainapp.signals