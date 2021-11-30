"""
dolbyio_rest_apis.core.rate_limiter
~~~~~~~~~~~~~~~

This module contains the rate limiter for the HTTP requests.
"""

import logging
import asyncio
import time

class RateLimiter:
    """
    Rate limiter for HTTP requests.
    """

    MAX_REQUESTS_PER_SECOND: int = 50

    def __init__(self):
        self._logger = logging.getLogger(RateLimiter.__name__)
        self._nb_requests_left = self.MAX_REQUESTS_PER_SECOND
        self._last_update = time.monotonic()

    async def wait_until_allowed(self):
        """
        Wait until the request is allowed to go through.
        """

        log_printed = False
        while self._nb_requests_left <= 0:
            if not log_printed:
                # Only print that message once
                log_printed = True
                self._logger.debug('This request is being throttled.')

            self._add_new_request()
            await asyncio.sleep(0.1)

        self._nb_requests_left -= 1

    def _add_new_request(self):
        now = time.monotonic()
        left = self._nb_requests_left + now - self._last_update
        if left > 0:
            self._nb_requests_left = min(left, self.MAX_REQUESTS_PER_SECOND)
            self._last_update = now

# Instance of the rate limiter to share across all APIs
RATE_LIMITER = RateLimiter()
