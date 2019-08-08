# Django
from django.apps import AppConfig


class SourceConfig(AppConfig):
    name = 'apps.source'
    verbose_name = 'Source Database'

    def ready(self):
        return
