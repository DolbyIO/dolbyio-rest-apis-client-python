"""
dolbyio_rest_apis.media.internal.helpers
~~~~~~~~~~~~~~~

This module contains internal helpers.
"""

from aiohttp import BasicAuth, ClientResponse, ContentTypeError
from dolbyio_rest_apis.core.helpers import get_value_or_default
from dolbyio_rest_apis.core.http_context import HttpContext
from dolbyio_rest_apis.core.http_request_error import HttpRequestError
import json
import logging
from typing import Any, Dict, Mapping

class MediaHttpContext(HttpContext):
    """HTTP Context class for Media APIs"""

    def __init__(self):
        super().__init__()

        self._logger = logging.getLogger(MediaHttpContext.__name__)

    async def _requests_post_put(
            self,
            access_token: str,
            url: str,
            method: str,
            payload: Any=None,
            params: Mapping[str, str]=None,
        ) -> Any or None:
        r"""
        Sends a POST or PUT request.

        Args:
            access_token: Access token to use for authentication.
            url: Where to send the request to.
            method: HTTP method, POST or PUT.
            payload: (Optional) Content of the request.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        if payload is None:
            payload = '{}' # The REST APIs don't support an empty payload
        elif not isinstance(payload, str):
            payload = json.dumps(payload, indent=4)

        return await self._send_request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            data=payload,
        )

    async def requests_post(
            self,
            access_token: str,
            url: str,
            payload: Any=None,
            params: Mapping[str, str]=None,
        ) -> Any or None:
        r"""
        Sends a POST request.

        Args:
            access_token: Access token to use for authentication.
            url: Where to send the request to.
            payload: (Optional) Content of the request.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        return await self._requests_post_put(
            access_token=access_token,
            url=url,
            method='POST',
            payload=payload,
            params=params,
        )

    async def requests_post_basic_auth(
            self,
            app_key: str,
            app_secret: str,
            url: str,
            data: Dict[str, Any],
        ) -> Any or None:
        r"""
        Sends a POST request with Basic authentication.

        Args:
            app_key: Your Dolby.io App Key.
            app_secret: Your Dolby.io App Secret.
            url: Where to send the request to.
            data: Content of the request.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        return await self._send_request(
            method='POST',
            url=url,
            headers=headers,
            auth=BasicAuth(app_key, app_secret),
            data=data,
        )

    async def requests_put(
            self,
            access_token: str,
            url: str,
            payload: Any=None,
            params: Mapping[str, str]=None,
        ) -> Any or None:
        r"""
        Sends a PUT request.

        Args:
            access_token: Access token to use for authentication.
            url: Where to send the request to.
            payload: (Optional) Content of the request.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        return await self._requests_post_put(
            access_token=access_token,
            url=url,
            method='PUT',
            payload=payload,
            params=params,
        )

    async def requests_get(
            self,
            access_token: str,
            url: str,
            params: Mapping[str, str]=None,
        ) -> Any or None:
        r"""
        Sends a GET request.

        Args:
            access_token: Access token to use for authentication.
            url: Where to send the request to.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        return await self._send_request(
            method='GET',
            url=url,
            params=params,
            headers=headers,
        )

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

    async def download(
            self,
            access_token: str,
            url: str,
            file_path: str,
            params: Mapping[str, str]=None,
        ) -> None:
        r"""
        Downloads a file.

        Args:
            access_token: Access token to use for authentication.
            url: Where to send the request to.
            file_path: Where to save the file.
            params: (Optional) URL query parameters.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/octet-stream',
            'Authorization': f'Bearer {access_token}',
        }

        await self._download_file(
            url=url,
            params=params,
            headers=headers,
            file_path=file_path
        )

    async def upload(
            self,
            upload_url: str,
            file_path: str
        ) -> None:
        r"""
        Uploads a file.

        Args:
            upload_url: URL where to upload the file to.
            file_path: Path of the file to upload.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        await self._upload_file(
            url=upload_url,
            file_path=file_path
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

                error_type = get_value_or_default(json_response, 'type', None)
                error_code = get_value_or_default(json_response, 'status', 0)
                error_reason = get_value_or_default(json_response, 'title', None)
                error_description = get_value_or_default(json_response, 'detail', None)

                raise HttpRequestError(http_response, error_type, error_code, error_reason, error_description)
            except (ValueError, ContentTypeError): # If the response body does not contain valid json.
                pass

        http_response.raise_for_status()
