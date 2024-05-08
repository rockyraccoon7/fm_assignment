from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'mainapp'

    def ready(self):
        import mainapp.signals