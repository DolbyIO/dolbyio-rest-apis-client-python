"""
dolbyio_rest_apis.communications.authentication
~~~~~~~~~~~~~~~

This module contains the functions to work with the authentication API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_comms_session_url
from dolbyio_rest_apis.models import AccessToken

async def get_client_access_token(
        app_key: str,
        app_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    This API returns an access token that your backend can request on behalf of a client to initialize
    the Dolby.io SDK in a secure way.

    See: https://docs.dolby.io/communications-apis/reference/get-client-access-token

    Args:
        app_key: Your Dolby.io App Key.
        app_secret: Your Dolby.io App Secret.
        expires_in: (Optional) Access token expiration time in seconds.
            The maximum value is 86,400, indicating 24 hours.
            If no value is specified, the default is 3,600, indicating one hour.

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
            url=f'{get_comms_session_url()}/oauth2/token',
            data=data
        )

    return AccessToken(json_response)
