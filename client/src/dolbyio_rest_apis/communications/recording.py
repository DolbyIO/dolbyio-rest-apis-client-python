"""
dolbyio_rest_apis.communications.recording
~~~~~~~~~~~~~~~

This module contains the functions to work with the recording API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_comms_url_v2

async def start(
        access_token: str,
        conference_id: str,
        layout_url: str=None,
        width: int=-1,
        height: int=-1,
        mix_id: str=None,
    ) -> None:
    r"""
    Starts recording for the specified conference.

    You can specify a custom layout URL per a recording request.
    The `layout_url` parameter overrides the layout URL configured in the dashboard.

    You can also specify the resolution of the recording.
    The default mixer layout application supports both 1920x1080 (16:9 aspect ratio) and 1080x1920 (9:16 aspect ratio).
    If the `width` and `height` parameters are not specified, then the system defaults to 1920x1080.

    Using the `mix_id` parameter you can uniquely identify individual mixed recordings.
    For example, `landscape-stage` and `portrait-audience` as mixId can help you identify the purpose of the recording
    when you receive the webhook notification or use the Monitor API to retrieve the recordings.
    You may start only one recording per mixId.

    See: https://docs.dolby.io/communications-apis/reference/api-recording-start

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        layout_url: (Optional) Overwrites the layout URL configuration.
            This field is ignored if it is not relevant regarding recording configuration,
            for example if live_recording set to false or if the recording is MP3 only.
            - `null`: uses the layout URL configured in the dashboard (if no URL is set in the dashboard, then uses the Dolby.io default);
            - `default`: uses the Dolby.io default layout;
            - URL string: uses this layout URL
        width: (Optional) The frame width can range between 390 and 1920 pixels and is set to 1920 by default.
        height: (Optional) The frame height can range between 390 and 1920 pixels and is set to 1080 by default.
        mix_id: (Optional) A unique identifier for you to identify individual mixes.
            You may only start one streaming per mixId.
            Not providing its value results in setting the `default` value.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_url_v2()}/conferences/mix/{conference_id}/recording/start'

    payload = {}
    add_if_not_none(payload, 'layoutUrl', layout_url)
    if width > 0:
        payload['width'] = width
    if height > 0:
        payload['height'] = height
    add_if_not_none(payload, 'mixId', mix_id)

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
