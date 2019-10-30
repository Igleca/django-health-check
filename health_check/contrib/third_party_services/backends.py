
import requests
from threading import Thread

from django.conf import settings

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException


class ThirdPartyServicesHealthCheck(BaseHealthCheckBackend):

    def fetch_url(self, url, results, i):
        timeout = getattr(settings, 'HTTP_REQUEST_TIMEOUT', 5)
        try:
            response = requests.get(url, timeout=timeout)
            if response.ok:
                msg = None
            else:
                msg = '%s -- is not OK. Returned %s' % (url,
                                                        response.status_code)
        except Exception as e:
            msg = '%s -- %s' % (url, str(e.__class__.__name__))

        results[i] = msg

    def check_status(self):
        urls = getattr(settings, 'HEALTHCHECK_THIRD_PARTY_URLS', [])

        total_urls = len(urls)
        threads = [None] * total_urls
        results = [None] * total_urls

        for i, url in enumerate(urls):
            threads[i] = Thread(target=self.fetch_url, args=(url, results, i))
            threads[i].start()

        for i in range(total_urls):
            threads[i].join()

        results = [result for result in results if result]
        if results:
            self.add_error(HealthCheckException(results))
