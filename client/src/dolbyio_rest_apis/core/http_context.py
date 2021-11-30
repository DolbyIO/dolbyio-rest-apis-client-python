"""
dolbyio_rest_apis.core.http_context
~~~~~~~~~~~~~~~

This module contains the HTTP Context class.
"""

import aiofiles
from aiohttp import BasicAuth, ClientResponse, ClientTimeout, ServerTimeoutError, ContentTypeError
from aiohttp_retry import RetryClient, JitterRetry
import datetime
import logging
from .rate_limiter import RATE_LIMITER
from typing import Any, Mapping, Optional, Type
from types import TracebackType

TOTAL_REQUEST_TIMEOUT: int = 60 # seconds
TOTAL_REQUEST_DOWNLOAD_FILE_TIMEOUT: int = 30 * 60 # 30 minutes
CONNECT_REQUEST_TIMEOUT: int = 25 # seconds

RETRY_MAX_ATTEMPTS: int = 3
RETRY_START_TIMEOUT: float = 1.0

class HttpContext:
    """
    HTTP Context used to send HTTP requests.
    """

    def __init__(self):
        self._logger = logging.getLogger(HttpContext.__name__)

        retry_options = JitterRetry(
            attempts=RETRY_MAX_ATTEMPTS,
            start_timeout=RETRY_START_TIMEOUT,
            random_interval_size=1.0,
            statuses=[ 502, 503 ],
            exceptions=[ ServerTimeoutError ],
        )

        self._session = RetryClient(
            raise_for_status=False,
            retry_options=retry_options,
        )

    async def close(self):
        if not self._session is None:
            await self._session.close()
            self._session = None

    def __enter__(self) -> None:
        raise TypeError('Use async with instead')

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        # __exit__ should exist in pair with __enter__ but never executed
        pass  # pragma: no cover

    async def __aenter__(self) -> 'HttpContext':
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def _download_file(
            self,
            url: str,
            headers: Mapping[str, str],
            file_path: str,
            params: Mapping[str, str]=None,
        ):
        self._logger.debug('GET %s', url)

        async with self._session.get(
            url,
            params=params,
            headers=headers,
            # By default aiohttp uses strict checks for HTTPS protocol.
            # Certification checks can be relaxed by setting ssl to False.
            ssl=False,
            timeout=ClientTimeout(total=TOTAL_REQUEST_DOWNLOAD_FILE_TIMEOUT, connect=CONNECT_REQUEST_TIMEOUT),
        ) as http_response:
            await self._raise_for_status(http_response)

            total_kb = 0

            async with aiofiles.open(file_path, mode='wb') as output_file:
                async for chunk in http_response.content.iter_chunked(1024):
                    total_kb += 1
                    if total_kb % 10240 == 0:
                        # Only print every 10 MB
                        self._logger.debug('Downloading %s - %.1f MB', file_path, total_kb / 1024)
                    await output_file.write(chunk)

            self._logger.debug('Downloaded %s - %.1f MB', file_path, total_kb / 1024)

    async def _upload_file(
            self,
            url: str,
            file_path: str,
        ):
        self._logger.debug('PUT %s', url)

        with open(file_path, 'rb') as input_file:
            await self._session.put(
                url,
                # By default aiohttp uses strict checks for HTTPS protocol.
                # Certification checks can be relaxed by setting ssl to False.
                ssl=False,
                data=input_file,
            )

    async def _send_request(
            self,
            method: str,
            url: str,
            headers: Mapping[str, str],
            params: Mapping[str, str]=None,
            auth: BasicAuth=None,
            data: Any=None,
        ) -> Any or None:
        if params is None:
            self._logger.debug('%s %s', method, url)
        else:
            self._logger.debug('%s %s %s', method, url, params)
        start = datetime.datetime.now()

        try:
            # Use the rate limited to let request going through
            await RATE_LIMITER.wait_until_allowed()

            async with self._session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                auth=auth,
                data=data,
                # By default aiohttp uses strict checks for HTTPS protocol.
                # Certification checks can be relaxed by setting ssl to False.
                ssl=False,
                timeout=ClientTimeout(total=TOTAL_REQUEST_TIMEOUT, connect=CONNECT_REQUEST_TIMEOUT),
            ) as http_response:
                end = datetime.datetime.now()
                span = end - start
                self._logger.debug('Elapsed %.3f seconds', span.total_seconds())

                await self._raise_for_status(http_response)

                return await http_response.json()
        except ContentTypeError:
            return None # No JSON content
        except ServerTimeoutError:
            self._logger.error('Unable to get data from the url %s because of a timeout.', url)
            self._logger.error('Timeout is set to %i seconds.', TOTAL_REQUEST_TIMEOUT)
            raise

    async def _raise_for_status(self, http_response: ClientResponse):
        raise NotImplementedError()
