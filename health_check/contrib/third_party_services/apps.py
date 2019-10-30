
from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.third_party_services'

    def ready(self):
        from .backends import ThirdPartyServicesHealthCheck

        plugin_dir.register(ThirdPartyServicesHealthCheck)
