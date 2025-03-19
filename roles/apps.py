from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'roles'

    def ready(self):
        import roles.signals  # Register signals