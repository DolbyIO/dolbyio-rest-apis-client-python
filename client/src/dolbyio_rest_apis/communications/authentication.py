"""
dolbyio_rest_apis.communications.authentication
~~~~~~~~~~~~~~~

This module contains the functions to work with the authentication API.
"""

from deprecated import deprecated
from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_api_v1_url, get_session_url
from .models import AccessToken

async def _get_access_token(
        url: str,
        consumer_key: str,
        consumer_secret: str,
        expires_in: int=None,
    ) -> AccessToken:

    data = {
        'grant_type': 'client_credentials',
    }
    add_if_not_none(data, 'expires_in', expires_in)

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=url,
            data=data
        )

    return AccessToken(json_response)

async def get_api_access_token(
        consumer_key: str,
        consumer_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    Gets an access token to authenticate for API calls.

    See: https://docs.dolby.io/communications-apis/reference/jwt

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        expires_in: (Optional) Access token expiration time in seconds.
            The maximum value is 2,592,000, indicating 30 days. If no value is specified, the default is 600,
            indicating ten minutes.

    Returns:
        An :class:`AccessToken` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    return await _get_access_token(f'{get_api_v1_url()}/auth/token', consumer_key, consumer_secret, expires_in)

async def get_client_access_token(
        consumer_key: str,
        consumer_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    Gets a client access token to authenticate a session.

    See: https://docs.dolby.io/communications-apis/reference/postoauthtoken

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        expires_in: (Optional) Access token expiration time in seconds.
            The maximum value is 2,592,000, indicating 30 days. If no value is specified, the default is 600,
            indicating ten minutes.

    Returns:
        An :class:`AccessToken` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    return await _get_access_token(f'{get_session_url()}/oauth2/token', consumer_key, consumer_secret, expires_in)

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def revoke_access_token(
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
    ) -> None:
    r"""
    Revokes the authentication token.

    See: https://docs.dolby.io/communications-apis/reference/postoauthtokenrevoke

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        access_token: The access token to revoke.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    data = {
        'access_token': access_token,
    }

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=f'{get_session_url()}/oauth2/invalidate',
            data=data
        )
