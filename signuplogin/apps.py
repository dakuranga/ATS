from django.apps import AppConfig


class SignuploginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signuplogin'

    def ready(self):
        import signuplogin.signals
