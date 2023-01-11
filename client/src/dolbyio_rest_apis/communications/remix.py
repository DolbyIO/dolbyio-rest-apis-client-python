"""
dolbyio_rest_apis.communications.remix
~~~~~~~~~~~~~~~

This module contains the functions to work with the remix API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_comms_url_v2
from dolbyio_rest_apis.core.helpers import add_if_not_none
from .models import RemixStatus

async def start(
        access_token: str,
        conference_id: str,
        layout_url: str=None,
        layout_name: str=None,
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
        layout_url: Overwrites the layout URL configuration:
            null: uses the layout URL configured in the dashboard
                (if no URL is set in the dashboard, then uses the Dolby.io default)
            default: uses the Dolby.io default layout
            URL string: uses this layout URL
        layout_name: Defines a name for the given layout URL, which makes layout identification
            easier for customers especially when the layout URL is not explicit.

    Returns:
        A :class:`RemixStatus` object that represents the status of the remix.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_url_v2()}/conferences/mix/{conference_id}/remix/start'

    payload = {}
    add_if_not_none(payload, 'layoutUrl', layout_url)
    add_if_not_none(payload, 'layoutName', layout_name)

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url=url,
            payload=payload,
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
    url = f'{get_comms_url_v2()}/conferences/mix/{conference_id}/remix/status'

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
        )

    return RemixStatus(json_response)
