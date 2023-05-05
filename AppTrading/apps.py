from django.apps import AppConfig


class ApptradingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppTrading'

    def ready(self):
        from AppTrading import refresh
        refresh.start()
