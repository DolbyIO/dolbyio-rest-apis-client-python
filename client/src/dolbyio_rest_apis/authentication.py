"""
dolbyio_rest_apis.authentication
~~~~~~~~~~~~~~~

This module contains the functions to work with the authentication API.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_api_url
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from .models import AccessToken

async def get_api_token(
        app_key: str,
        app_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    To make any API call, you must acquire a JWT (JSON Web Token) format API token.

    See: https://docs.dolby.io/communications-apis/reference/get-api-token
    
    See: https://docs.dolby.io/media-apis/reference/get-api-token

    Args:
        app_key: Your Dolby.io App Key.
        app_secret: Your Dolby.io App Secret.
        expires_in: (Optional) API token expiration time in seconds.
            The maximum value is 86,400, indicating 24 hours.
            If no value is specified, the default is 1800, indicating 30 minutes.

    Returns:
        An :class:`AccessToken` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    data = {
        'grant_type': 'client_credentials',
    }
    add_if_not_none(data, 'expires_in', expires_in)

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post_basic_auth(
            app_key=app_key,
            app_secret=app_secret,
            url=f'{get_api_url()}/auth/token',
            data=data
        )

    return AccessToken(json_response)
