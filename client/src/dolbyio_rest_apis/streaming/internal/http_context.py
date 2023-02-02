"""
dolbyio_rest_apis.streaming.internal.helpers
~~~~~~~~~~~~~~~

This module contains internal helpers.
"""

from aiohttp import ClientResponse, ContentTypeError
from dolbyio_rest_apis.core.http_context import HttpContext
from dolbyio_rest_apis.core.http_request_error import HttpRequestError
from dolbyio_rest_apis.streaming.models.core import BaseResponse, Error
import json
import logging
from typing import Any, Mapping

class StreamingHttpContext(HttpContext):
    """HTTP Context class for Real-time Streaming APIs"""

    def __init__(self):
        super().__init__()

        self._logger = logging.getLogger(StreamingHttpContext.__name__)

    async def _requests_post_put(
            self,
            api_secret: str,
            url: str,
            method: str,
            payload: Any=None,
            params: Mapping[str, str]=None,
        ) -> dict:
        r"""
        Sends a POST or PUT request.

        Args:
            api_secret: API secret to use for authentication.
            url: Where to send the request to.
            method: HTTP method, POST or PUT.
            payload: (Optional) Content of the request.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_secret}',
        }

        if not isinstance(payload, str):
            payload = json.dumps(payload, indent=4)

        json_response = await self._send_request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            data=payload,
        )

        base = BaseResponse(json_response)
        return base.data

    async def requests_post(
            self,
            api_secret: str,
            url: str,
            payload: Any=None,
            params: Mapping[str, str]=None,
        ) -> dict:
        r"""
        Sends a POST request.

        Args:
            api_secret: API secret to use for authentication.
            url: Where to send the request to.
            payload: (Optional) Content of the request.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        return await self._requests_post_put(
            api_secret=api_secret,
            url=url,
            method='POST',
            payload=payload,
            params=params,
        )

    async def requests_put(
            self,
            api_secret: str,
            url: str,
            payload: Any=None,
            params: Mapping[str, str]=None,
        ) -> dict:
        r"""
        Sends a PUT request.

        Args:
            api_secret: API secret to use for authentication.
            url: Where to send the request to.
            payload: (Optional) Content of the request.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        return await self._requests_post_put(
            api_secret=api_secret,
            url=url,
            method='PUT',
            payload=payload,
            params=params,
        )

    async def requests_get(
            self,
            api_secret: str,
            url: str,
            params: Mapping[str, str]=None,
        ) -> dict:
        r"""
        Sends a GET request.

        Args:
            api_secret: API secret to use for authentication.
            url: Where to send the request to.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_secret}',
        }

        json_response = await self._send_request(
            method='GET',
            url=url,
            params=params,
            headers=headers,
        )

        base = BaseResponse(json_response)
        return base.data

    async def requests_delete(
            self,
            access_token: str,
            url: str,
            params: Mapping[str, str]=None,
        ) -> None:
        r"""
        Sends a DELETE request.

        Args:
            access_token: Access token to use for authentication.
            url: Where to send the request to.
            params: (Optional) URL query parameters.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        return await self._send_request(
            method='DELETE',
            url=url,
            params=params,
            headers=headers,
        )

    async def _raise_for_status(self, http_response: ClientResponse):
        r"""Raises :class:`HttpRequestError` or :class:`ClientResponseError`, if one occurred."""

        if 400 <= http_response.status < 500:
            if 400 < http_response.status < 404:
                self._logger.error('Unauthorized to get data from the url %s - Response code %i', http_response.url, http_response.status)
            elif http_response.status == 404:
                self._logger.error('Unable to get data from the url %s - Not found (404)', http_response.url)
            else:
                self._logger.error('Did not find data at the url %s - Response code %i', http_response.url, http_response.status)

            try:
                json_response = await http_response.json()
                base_response = BaseResponse(json_response)
                err = Error(base_response.data)

                raise HttpRequestError(http_response, '', http_response.status, base_response.status, err.message)
            except (ValueError, ContentTypeError): # If the response body does not contain valid json.
                pass

        http_response.raise_for_status()
