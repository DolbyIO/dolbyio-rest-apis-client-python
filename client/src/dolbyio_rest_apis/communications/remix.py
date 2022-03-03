"""
dolbyio_rest_apis.communications.remix
~~~~~~~~~~~~~~~

This module contains the functions to work with the remix API.
"""

from deprecated import deprecated
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_api_v2_url, get_session_url
from .models import RemixStatus

async def start(
        access_token: str,
        conference_id: str,
    ) -> RemixStatus:
    r"""
    Remix a conference.

    Use this API to trigger a remix and regenerate a recording of a previously recorded conference using
    the current mixer layout. The `Recording.MP4.Available` event is sent if the customer has configured
    the webhook in the developer portal.

    See: https://docs.dolby.io/communications-apis/reference/start-conference-remix

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Returns:
        A :class:`RemixStatus` object that represents the status of the remix.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_api_v2_url()}/conferences/mix/{conference_id}/remix/start'

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url=url,
        )

    return RemixStatus(json_response)

async def get_status(
        access_token: str,
        conference_id: str,
    ) -> RemixStatus:
    r"""
    Get the status of a current mixing job. You must use this API if the conference is protected
    using enhanced conference access control.

    See: https://docs.dolby.io/communications-apis/reference/get-conference-remix-status

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Returns:
        A :class:`RemixStatus` object that represents the status of the remix.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_api_v2_url()}/conferences/mix/{conference_id}/remix/status'

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
        )

    return RemixStatus(json_response)

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def start_basic_auth(
        consumer_key: str,
        consumer_secret: str,
        conference_id: str,
    ) -> RemixStatus:
    r"""
    Remix a conference.

    Use this API to trigger a remix and regenerate a recording of a previously recorded conference using
    the current mixer layout. The `Recording.MP4.Available` event is sent if the customer has configured
    the webhook in the developer portal.

    See: https://docs.dolby.io/communications-apis/reference/start-conference-remix-v1

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        conference_id: Identifier of the conference.

    Returns:
        A :class:`RemixStatus` object that represents the status of the remix.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_session_url()}/api/conferences/mix/{conference_id}/record'

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=url,
        )

    return RemixStatus(json_response)

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def get_status_basic_auth(
        consumer_key: str,
        consumer_secret: str,
        conference_id: str,
    ) -> RemixStatus:
    r"""
    Get the status of a current mixing job.

    See: https://docs.dolby.io/communications-apis/reference/get-conference-remix-status-v1

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        conference_id: Identifier of the conference.

    Returns:
        A :class:`RemixStatus` object that represents the status of the remix.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_session_url()}/api/conferences/mix/{conference_id}/status'

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=url,
        )

    return RemixStatus(json_response)
