"""
dolbyio_rest_apis.media.platform
~~~~~~~~~~~~~~~

This module contains the functions to work with the Platform APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.access_token import AccessToken

async def get_access_token(
        api_key: str,
        api_secret: str,
    ) -> AccessToken:
    r"""
    Generates OAuth2 access token.

    Generates an access token to be used for Bearer Authentication for Media API calls.
    The token will expire in 12 hours.

    See: https://docs.dolby.io/media-apis/reference/media-oauth2-post

    Args:
        api_key: Your Dolby.io API Key.
        api_secret: Your Dolby.io API Secret.

    Returns:
        An :class:`AccessToken` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    data = {
        'grant_type': 'client_credentials',
    }

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post_basic_auth(
            api_key=api_key,
            api_secret=api_secret,
            url='https://api.dolby.com/media/oauth2/token',
            data=data
        )

    return AccessToken(json_response)
