from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'mechanical_express'

    def ready(self):
        import mechanical_express.signals  # Asegúrate de que 'myapp' es el nombre de tu aplicación
