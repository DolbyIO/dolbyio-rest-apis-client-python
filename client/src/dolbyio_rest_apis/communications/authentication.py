"""
dolbyio_rest_apis.communications.authentication
~~~~~~~~~~~~~~~

This module contains the functions to work with the authentication API.
"""

from deprecated import deprecated
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_comms_session_url, get_comms_url_v2
from dolbyio_rest_apis.models import AccessToken
from typing import List

@deprecated(reason='''
    This function is now deprecated and will be removed in the next release of this SDK.
    Please start using :meth:`get_client_access_token_v2` instead.
    ''')
async def get_client_access_token(
        app_key: str,
        app_secret: str,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    This API returns an access token that your backend can request on behalf of a client to initialize
    the Dolby.io SDK in a secure way.

    See: https://docs.dolby.io/communications-apis/reference/get-client-access-token-v1

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

async def get_client_access_token_v2(
        access_token: str,
        session_scope: List[str],
        external_id: str=None,
        expires_in: int=None,
    ) -> AccessToken:
    r"""
    This API returns an access token that your backend can request on behalf of a client to initialize
    the Dolby.io SDK in a secure way.

    See: https://docs.dolby.io/communications-apis/reference/get-client-access-token

    Args:
        access_token: Access token to use for authentication.
        session_scope: A list of case-sensitive strings allowing you to control
            what scope of access the client access token should have.
            The API supports the following scopes:
                - conf:create: Allows creating a new conference.
                - notifications:set: Allows the client to subscribe to events.
                - file:convert: Allows converting files.
                - session:update: Allows updating the participant's name and avatar URL.
            Incorrect values are omitted. If you want to give the token access to all scopes, you can use a wildcard, such as *.
        external_id: (Optional) The unique identifier of the participant who requests the token.
        expires_in: (Optional) Access token expiration time in seconds.
            If no value is specified, the default is 3,600, indicating one hour.
            The maximum value is 86,400, indicating 24 hours.
    Returns:
        An :class:`AccessToken` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    payload = {}
    add_if_not_none(payload, 'externalId', external_id)
    add_if_not_none(payload, 'expires_in', expires_in)
    if session_scope is not None:
        payload['sessionScope'] = ' '.join(session_scope)

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/client-access-token',
            payload=payload,
        )

    return AccessToken(json_response)
