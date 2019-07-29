# Django
from django.apps import AppConfig


class BhsConfig(AppConfig):
    name = 'apps.bhs'
    verbose_name = 'BHS Member Center'

    def ready(self):
        return
