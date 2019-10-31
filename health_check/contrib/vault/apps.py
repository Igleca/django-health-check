
from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.vault'

    def ready(self):
        from .backends import VaultHealthCheck

        plugin_dir.register(VaultHealthCheck)
