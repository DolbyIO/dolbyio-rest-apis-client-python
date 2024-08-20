"""
dolbyio_rest_apis.streaming.stream
~~~~~~~~~~~~~~~

This module contains the functions to work with the Stream APIs.
"""

from dolbyio_rest_apis.core.urls import get_rts_url
from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.models.stream import StreamStoppingLevel

async def stop(
        api_secret: str,
        stream_id: str,
    ) -> None:
    payload = {
        'streamId': stream_id,
    }

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_post(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/stream/stop',
            payload=payload,
        )

    return StreamStoppingLevel.from_dict(dict_data)

async def stop_all(
        api_secret: str,
    ) -> None:
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_post(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/stream/stop/all',
        )

    return StreamStoppingLevel.from_dict(dict_data)
