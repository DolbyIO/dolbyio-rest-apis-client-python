"""
dolbyio_rest_apis.communications.authentication
~~~~~~~~~~~~~~~

This module contains the functions to work with the authentication API.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_api_url, get_session_url
from .models import AccessToken

async def _get_access_token(
        url: str,
        app_key: str,
        app_secret: str,
        expires_in: int=None,
    ) -> AccessToken:

    data = {
        'grant_type': 'client_credentials',
    }
    add_if_not_none(data, 'expires_in', expires_in)

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post_basic_auth(
            app_key=app_key,
            app_secret=app_secret,
            url=url,
            data=data
        )

    return AccessToken(json_response)

async def get_api_token(
        app_key: str,
        app_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    To make any API call, you must acquire a JWT (JSON Web Token) format API token.
    Make sure to use this API against https://api.dolby.io/v1.

    Note: Even though the OAuth terminology is used in the following APIs, they are not OAuth compliant.

    See: https://docs.dolby.io/communications-apis/reference/get-api-token

    Args:
        app_key: Your Dolby.io App Key.
        app_secret: Your Dolby.io App Secret.
        expires_in: (Optional) API token expiration time in seconds.
            The maximum value is 2,592,000, indicating 30 days.
            If no value is specified, the default is 1800, indicating 30 minutes.

    Returns:
        An :class:`AccessToken` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    return await _get_access_token(f'{get_api_url()}/auth/token', app_key, app_secret, expires_in)

async def get_client_access_token(
        app_key: str,
        app_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    This API returns an access token that your backend can request on behalf of a client to initialize
    the Dolby.io SDK in a secure way. Make sure to use this API against https://session.voxeet.com.

    Note: Even though the OAuth2 terminology is used in the following APIs, they are not OAuth2 compliant.

    See: https://docs.dolby.io/communications-apis/reference/get-client-access-token

    Args:
        app_key: Your Dolby.io App Key.
        app_secret: Your Dolby.io App Secret.
        expires_in: (Optional) Access token expiration time in seconds.
            The maximum value is 2,592,000, indicating 30 days. If no value is specified, the default is 600,
            indicating ten minutes.

    Returns:
        An :class:`AccessToken` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    return await _get_access_token(f'{get_session_url()}/oauth2/token', app_key, app_secret, expires_in)
