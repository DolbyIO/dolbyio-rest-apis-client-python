"""
dolbyio_rest_apis.communications.streaming
~~~~~~~~~~~~~~~

This module contains the functions to work with the streaming API.
"""

from deprecated import deprecated
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_api_v2_url, get_session_url
from typing import List

async def start_rtmp(
        access_token: str,
        conference_id: str,
        rtmp_urls: List[str],
    ) -> None:
    r"""
    Starts an RTMP live stream. Once the Dolby Interactivity API service started streaming to the target url,
    a `Stream.Rtmp.InProgress` Webhook event will be sent. You must use this API if the conference is protected
    using enhanced conference access control.

    See: https://docs.dolby.io/interactivity/reference/postrtmpstart

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
            url=f'{get_api_v2_url()}/conferences/mix/{conference_id}/rtmp/start',
            payload=payload
        )

async def stop_rtmp(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops an RTMP stream. You must use this API if the conference is protected using enhanced conference access control.

    See: https://docs.dolby.io/interactivity/reference/postrtmpstop

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
            url=f'{get_api_v2_url()}/conferences/mix/{conference_id}/rtmp/stop'
        )

async def start_hls(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Starts an HTTP Live Stream (HLS). The HLS URL is included in the Stream.Hls.InProgress Webhook event.
    You must use this API if the conference is protected using enhanced conference access control.

    See: https://docs.dolby.io/interactivity/reference/posthlsstart

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
            url=f'{get_api_v2_url()}/conferences/mix/{conference_id}/hls/start'
        )

async def stop_hls(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops an HTTP Live Stream (HLS). You must use this API if the conference is protected
    using enhanced conference access control.

    See: https://docs.dolby.io/interactivity/reference/posthlsstop

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
            url=f'{get_api_v2_url()}/conferences/mix/{conference_id}/hls/stop'
        )

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def start_rtmp_basic_auth(
        consumer_key: str,
        consumer_secret: str,
        conference_id: str,
        rtmp_urls: List[str],
    ) -> None:
    r"""
    Starts an RTMP live stream. Once the Dolby Interactivity API service started streaming to the target url,
    a `Stream.Rtmp.InProgress` Webhook event will be sent.

    See: https://docs.dolby.io/interactivity/reference/postrtmpstartv1

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
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
        await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=f'{get_session_url()}/api/conferences/mix/{conference_id}/live/start',
            json_payload=payload
        )

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def stop_rtmp_basic_auth(
        consumer_key: str,
        consumer_secret: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops an RTMP stream.

    See: https://docs.dolby.io/interactivity/reference/postrtmpstopv1

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=f'{get_session_url()}/api/conferences/mix/{conference_id}/live/stop'
        )

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def start_hls_basic_auth(
        consumer_key: str,
        consumer_secret: str,
        conference_id: str,
    ) -> None:
    r"""
    Starts an HTTP Live Stream (HLS). The HLS URL is included in the Stream.Hls.InProgress Webhook event.

    See: https://docs.dolby.io/interactivity/reference/posthlsstartv1

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=f'{get_session_url()}/api/conferences/mix/{conference_id}/hls/start'
        )

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def stop_hls_basic_auth(
        consumer_key: str,
        consumer_secret: str,
        conference_id: str,
    ) -> None:
    r"""
    Stops an HTTP Live Stream (HLS).

    See: https://docs.dolby.io/interactivity/reference/posthlsstopv1

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=f'{get_session_url()}/api/conferences/mix/{conference_id}/hls/stop'
        )
