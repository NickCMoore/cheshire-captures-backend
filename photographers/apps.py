from django.apps import AppConfig

class PhotographersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photographers'

    def ready(self):
        # Import signals to ensure they are registered
        import photographers.signals
