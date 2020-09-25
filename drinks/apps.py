from django.apps import AppConfig


class DrinksConfig(AppConfig):
    name = 'drinks'

    def ready(self):
        import drinks.signals