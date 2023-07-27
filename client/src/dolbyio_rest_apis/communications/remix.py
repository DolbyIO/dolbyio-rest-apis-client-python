"""
dolbyio_rest_apis.communications.remix
~~~~~~~~~~~~~~~

This module contains the functions to work with the remix API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_comms_url_v2
from .models import RemixStatus

async def start(
        access_token: str,
        conference_id: str,
        layout_url: str=None,
        width: int=-1,
        height: int=-1,
        mix_id: str=None,
    ) -> RemixStatus:
    r"""
    Remix a conference.

    Triggers a remix and regenerates a recording of a previously recorded conference
    using a [mixer layout](https://docs.dolby.io/communications-apis/docs/guides-mixer-layout).
    You can remix only one conference at a time.
    The `Recordings.Available` event is sent if the customer has configured the webhook in the developer portal.
    For more information, see the [Recording Conferences](https://docs.dolby.io/communications-apis/docs/guides-recording-conferences)
    and [Multiple Layout Mixes](https://docs.dolby.io/communications-apis/docs/guides-multiple-layout-mixes) documents.
    
    You can also specify the resolution of the remix.
    The default mixer layout application supports both 1920x1080 (16:9 aspect ratio) and 1080x1920 (9:16 aspect ratio).
    If the `width` and `height` parameters are not specified, then the system defaults to 1920x1080.

    See: https://docs.dolby.io/communications-apis/reference/start-conference-remix

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        layout_url: (Optional) Overwrites the layout URL configuration:
            null: uses the layout URL configured in the dashboard
                (if no URL is set in the dashboard, then uses the Dolby.io default)
            default: uses the Dolby.io default layout
            URL string: uses this layout URL
        width: (Optional) The frame width can range between 390 and 1920 pixels and is set to 1920 by default.
        height: (Optional) The frame height can range between 390 and 1920 pixels and is set to 1080 by default.
        mix_id: (Optional) A unique identifier for you to identify individual mixes.
            You may only start one streaming per mixId.
            Not providing its value results in setting the `default` value.

    Returns:
        A :class:`RemixStatus` object that represents the status of the remix.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_url_v2()}/conferences/mix/{conference_id}/remix/start'

    payload = {}
    add_if_not_none(payload, 'layoutUrl', layout_url)
    if width > 0:
        payload['width'] = width
    if height > 0:
        payload['height'] = height
    add_if_not_none(payload, 'mixId', mix_id)

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
