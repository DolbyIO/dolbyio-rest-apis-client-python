"""
dolbyio_rest_apis.communications.recording
~~~~~~~~~~~~~~~

This module contains the functions to work with the recording API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_comms_url_v2
from dolbyio_rest_apis.core.helpers import add_if_not_none

async def start(
        access_token: str,
        conference_id: str,
        layout_url: str=None,
    ) -> None:
    r"""
    Starts recording for the specified conference.
    You can specify a custom layout URL per recording request.
    The `layoutURL` parameter overrides the layout URL configured in the dashboard.

    See: https://docs.dolby.io/communications-apis/reference/api-recording-start

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        layout_url: Overwrites the layout URL configuration.
            This field is ignored if it is not relevant regarding recording configuration,
            for example if live_recording set to false or if the recording is MP3 only.
            - `null`: uses the layout URL configured in the dashboard (if no URL is set in the dashboard, then uses the Dolby.io default);
            - `default`: uses the Dolby.io default layout;
            - URL string: uses this layout URL

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_url_v2()}/conferences/mix/{conference_id}/recording/start'

    payload = {}
    add_if_not_none(payload, 'layoutUrl', layout_url)

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=url,
            payload=payload,
        )

async def stop(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops the recording of the specified conference.

    See: https://docs.dolby.io/communications-apis/reference/api-recording-stop

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_url_v2()}/conferences/mix/{conference_id}/recording/stop'

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=url,
        )
