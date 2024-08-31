from django.apps import AppConfig


class CarepathConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CarePath'

    # def ready(self):
    #     import CarePath.signals
