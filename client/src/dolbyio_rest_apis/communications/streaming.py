"""
dolbyio_rest_apis.communications.streaming
~~~~~~~~~~~~~~~

This module contains the functions to work with the streaming API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_comms_url_v2
from .models import RtsStream

async def start_rtmp(
        access_token: str,
        conference_id: str,
        rtmp_url: str,
        layout_url: str=None,
        width: int=-1,
        height: int=-1,
        mix_id: str=None,
    ) -> None:
    r"""
    Starts the RTMP live stream for the specified conference. Once the Dolby.io Communications APIs service starts
    streaming to the target url, a `Stream.Rtmp.InProgress` Webhook event will be sent.
    
    You can also specify the resolution of the RTMP stream.
    The default mixer layout application supports both 1920x1080 (16:9 aspect ratio) and 1080x1920 (9:16 aspect ratio).
    If the `width` and `height` parameters are not specified, then the system defaults to 1920x1080.

    See: https://docs.dolby.io/communications-apis/reference/start-rtmp

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        rtmp_url: The destination URI provided by the RTMP service.
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

    payload = {
        'uri': rtmp_url,
    }
    add_if_not_none(payload, 'layoutUrl', layout_url)
    if width > 0:
        payload['width'] = width
    if height > 0:
        payload['height'] = height
    add_if_not_none(payload, 'mixId', mix_id)

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/mix/{conference_id}/rtmp/start',
            payload=payload
        )

async def stop_rtmp(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops the RTMP stream of the specified conference.

    See: https://docs.dolby.io/communications-apis/reference/stop-rtmp

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/mix/{conference_id}/rtmp/stop'
        )

async def start_rts(
        access_token: str,
        conference_id: str,
        layout_url: str=None,
        width: int=-1,
        height: int=-1,
        mix_id: str=None,
    ) -> RtsStream:
    r"""
    Starts real-time streaming using Dolby.io Real-time Streaming services (formerly Millicast).
    
    You can also specify the resolution of the RTS stream.
    The default mixer layout application supports both 1920x1080 (16:9 aspect ratio) and 1080x1920 (9:16 aspect ratio).
    If the `width` and `height` parameters are not specified, then the system defaults to 1920x1080.

    See: https://docs.dolby.io/communications-apis/reference/start-rts

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        stream_name: The Dolby.io Real-time Streaming stream name to which the conference is broadcasted.
        publishing_token: The publishing token used to identify the broadcaster.
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
        A :class:`RtsStream` object that represents the status of the remix.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

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
            url=f'{get_comms_url_v2()}/conferences/mix/{conference_id}/rts/start',
            payload=payload,
        )

async def stop_rts(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops real-time streaming to Dolby.io Real-time Streaming services.

    See: https://docs.dolby.io/communications-apis/reference/stop-rts

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/mix/{conference_id}/rts/stop'
        )
