"""
dolbyio_rest_apis.communications.streaming
~~~~~~~~~~~~~~~

This module contains the functions to work with the streaming API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_comms_url_v2
from dolbyio_rest_apis.core.helpers import add_if_not_none
from typing import List

async def start_rtmp(
        access_token: str,
        conference_id: str,
        rtmp_url: str,
    ) -> None:
    r"""
    Starts the RTMP live stream for the specified conference. Once the Dolby.io Communications APIs service starts
    streaming to the target url, a `Stream.Rtmp.InProgress` Webhook event will be sent.

    See: https://docs.dolby.io/communications-apis/reference/start-rtmp

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        rtmp_urls: List of the RTMP endpoints where to send the RTMP stream to.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    payload = {
        'uri': rtmp_url,
    }

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
        stream_name: str,
        publishing_token: str,
        layout_url: str=None,
    ) -> None:
    r"""
    Starts real-time streaming using Dolby.io Real-time Streaming services (formerly Millicast).

    See: https://docs.dolby.io/communications-apis/reference/start-rts

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        stream_name: The Dolby.io Real-time Streaming stream name to which the conference is broadcasted.
        publishing_token: The publishing token used to identify the broadcaster.
        layout_url: Overwrites the layout URL configuration:
            null: uses the layout URL configured in the dashboard
                (if no URL is set in the dashboard, then uses the Dolby.io default)
            default: uses the Dolby.io default layout
            URL string: uses this layout URL

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    payload = {
        'stream_name': stream_name,
        'publishingToken': publishing_token,
    }
    add_if_not_none(payload, 'layoutUrl', layout_url)

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
