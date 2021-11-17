"""
dolbyio_rest_apis.core.http_context
~~~~~~~~~~~~~~~

This module contains the HTTP Context class.
"""

import aiofiles
import aiohttp
from aiohttp import BasicAuth, ClientResponse, ClientTimeout, ServerTimeoutError, ContentTypeError
import datetime
from sty import fg
from typing import Any, Mapping, Optional, Type
from types import TracebackType

TOTAL_REQUEST_TIMEOUT = 60 # seconds
CONNECT_REQUEST_TIMEOUT = 25 # seconds

class HttpContext:
    """
    HTTP Context used to send HTTP requests.
    """

    def __init__(self, log_verbose: bool=False):
        self.log_verbose = log_verbose
        self._session = aiohttp.ClientSession()

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
        if self.log_verbose:
            print(f'{fg.li_yellow}[http]{fg.rs} GET {url}')

        async with self._session.get(
            url,
            params=params,
            headers=headers,
            # By default aiohttp uses strict checks for HTTPS protocol.
            # Certification checks can be relaxed by setting ssl to False.
            ssl=False,
        ) as http_response:
            await self._raise_for_status(http_response)

            total_bits = 0

            async with aiofiles.open(file_path, mode='wb') as output_file:
                async for chunk in http_response.content.iter_chunked(1024):
                    if self.log_verbose:
                        total_bits += 1
                        print(f'{fg.yellow}Downloading{fg.rs} {file_path} [{total_bits / 1024:0.1f}]MB\r', end='')
                    await output_file.write(chunk)

            if self.log_verbose:
                print(f'{fg.green}Downloaded{fg.rs} {file_path} - {total_bits / 1024:0.1f} MB ')

    async def _upload_file(
            self,
            url: str,
            file_path: str,
        ):
        if self.log_verbose:
            print(f'{fg.li_yellow}[http]{fg.rs} PUT {url}')

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
        if self.log_verbose:
            if params is None:
                print(f'{fg.li_yellow}[http]{fg.rs} {method} {url}')
            else:
                print(f'{fg.li_yellow}[http]{fg.rs} {method} {url}', params)
            start = datetime.datetime.now()

        try:
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
                if self.log_verbose:
                    end = datetime.datetime.now()
                    span = end - start
                    print(f'{fg.li_yellow}[http]{fg.rs} Elapsed {span.total_seconds():.3f} seconds')

                await self._raise_for_status(http_response)

                return await http_response.json()
        except ContentTypeError:
            return None # No JSON content
        except ServerTimeoutError:
            print(f'{fg.red}[error]{fg.rs} Unable to get data from the url {url} because of a timeout.')
            print(f'{fg.red}[error]{fg.rs} Timeout is set to {TOTAL_REQUEST_TIMEOUT} seconds.')
            raise

    async def _raise_for_status(self, http_response: ClientResponse):
        raise NotImplementedError()
