"""
dolbyio_rest_apis.authentication
~~~~~~~~~~~~~~~

This module contains the functions to work with the authentication API.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_api_url
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from .models import AccessToken
from typing import List

async def get_api_token(
        app_key: str,
        app_secret: str,
        expires_in: int=None,
        scope: List[str]=None,
    ) -> AccessToken:
    r"""
    To make any API call, you must acquire a JWT (JSON Web Token) format API token.

    See: https://docs.dolby.io/communications-apis/reference/get-api-token
    
    See: https://docs.dolby.io/media-apis/reference/get-api-token

    Args:
        app_key: Your Dolby.io App Key.
        app_secret: Your Dolby.io App Secret.
        expires_in: (Optional) API token expiration time in seconds.
            If no value is specified, the default is 1800, indicating 30 minutes.
            The maximum value is 86,400, indicating 24 hours.
        scope: (Optional) A list of case-sensitive strings allowing you to control what scope of access the API token should have.
            If not specified, the API token will possess unrestricted access to all resources and actions.
            The API supports the following scopes:
                - comms:client_access_token:create: Allows requesting a client access token.
                - comms:conf:create: Allows creating a new conference.
                - comms:conf:admin: Allows administrating a conference, including actions
                    such as Invite, Kick, Send Message, Set Spatial Listener's Audio, and Update Permissions.
                - comms:conf:destroy: Allows terminating a live conference.
                - comms:monitor:delete: Allows deleting data from the Monitor API, for example, deleting recordings.
                - comms:monitor:read: Allows reading data through the Monitor API.
                - comms:monitor:download: Allows generating download URLs for data (e.g. recording) through the Monitor API.
                - comms:stream:write: Allows starting and stopping RTMP or Real-Time streaming.
                - comms:remix:write: Allows remixing recordings.
                - comms:remix:read: Allows reading the remix status.
                - comms:record:write: Allows starting and stopping recordings.
            Incorrect values are omitted. If you want to give the token access to all Communications REST APIs,
            you can use a wildcard, such as comms:*

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
    if scope is not None:
        data['scope'] = ' '.join(scope)

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post_basic_auth(
            app_key=app_key,
            app_secret=app_secret,
            url=f'{get_api_url()}/auth/token',
            data=data
        )

    return AccessToken(json_response)
