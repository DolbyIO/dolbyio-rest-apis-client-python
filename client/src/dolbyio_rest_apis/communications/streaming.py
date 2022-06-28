"""
dolbyio_rest_apis.communications.streaming
~~~~~~~~~~~~~~~

This module contains the functions to work with the streaming API.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_comms_url_v2
from typing import List

async def start_rtmp(
        access_token: str,
        conference_id: str,
        rtmp_urls: List[str],
    ) -> None:
    r"""
    Starts the RTMP live stream for the specified conference. Once the Dolby.io Communications APIs service starts
    streaming to the target url, a `Stream.Rtmp.InProgress` Webhook event will be sent.
    You must use this API if the conference is protected using enhanced conference access control.

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
        'uri': '|'.join(rtmp_urls),
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
    Stops an RTMP stream.
    You must use this API if the conference is protected using enhanced conference access control.

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

async def start_lls(
        access_token: str,
        conference_id: str,
        stream_name: str,
        publishing_token: str,
    ) -> None:
    r"""
    Starts a Low Latency Stream to Millicast.

    See: https://docs.dolby.io/communications-apis/reference/start-rtmp

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        stream_name: The Millicast stream name to which the conference will broadcasted.
        publishing_token:The Millicast publishing token used to identify the broadcaster.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    payload = {
        'stream_name': stream_name,
        'publishingToken': publishing_token,
    }

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/mix/{conference_id}/lls/start',
            payload=payload,
        )

async def stop_lls(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops an existing Low Latency Stream to Millicast.

    See: https://docs.dolby.io/communications-apis/reference/stop-lls

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
            url=f'{get_comms_url_v2()}/conferences/mix/{conference_id}/lls/stop'
        )
