
import requests

from django.conf import settings

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException


class VaultHealthCheck(BaseHealthCheckBackend):

    def check_status(self):
        url = getattr(settings, 'HEALTHCHECK_VAULT_URL', None)
        timeout = getattr(settings, 'HTTP_REQUEST_TIMEOUT', 5)

        if not url:
            return

        error = None
        try:
            response = requests.get(url, timeout=timeout)
            if not response.ok:
                error = 'Vault is not OK. Returned %s' % (response.status_code)
            else:
                if response.get('sealed'):
                    error = 'Vault is sealed'
        except Exception as e:
            error = 'Vault Exception -- %s' % (str(e.__class__.__name__))

        if error:
            self.add_error(HealthCheckException(error))
