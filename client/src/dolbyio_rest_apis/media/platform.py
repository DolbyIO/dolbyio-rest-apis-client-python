"""
dolbyio_rest_apis.media.platform
~~~~~~~~~~~~~~~

This module contains the functions to work with the Platform APIs.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.access_token import AccessToken

async def get_api_token(
        app_key: str,
        app_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    To make any API call, you must acquire a JWT (JSON Web Token) format API token.
    Make sure to use this API against https://api.dolby.io/v1.

    Note: Even though the OAuth terminology is used in the following APIs, they are not OAuth compliant.

    See: https://docs.dolby.io/media-apis/reference/get-api-token

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

    data = {
        'grant_type': 'client_credentials',
    }
    add_if_not_none(data, 'expires_in', expires_in)

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post_basic_auth(
            app_key=app_key,
            app_secret=app_secret,
            url='https://api.dolby.io/v1/auth/token',
            data=data
        )

    return AccessToken(json_response)
