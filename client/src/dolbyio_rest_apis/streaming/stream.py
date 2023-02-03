"""
dolbyio_rest_apis.streaming.stream
~~~~~~~~~~~~~~~

This module contains the functions to work with the Stream APIs.
"""

from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.internal.urls import SAPI_URL

async def stop(
        api_secret: str,
        account_id: str,
        stream_name: str,
    ) -> None:
    payload = {
        'streamId': f'{account_id}/{stream_name}',
    }

    async with StreamingHttpContext() as http_context:
        await http_context.requests_post(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/stream/stop',
            payload=payload,
        )

async def stop_all(
        api_secret: str,
    ) -> None:
    async with StreamingHttpContext() as http_context:
        await http_context.requests_post(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/stream/stop/all',
        )
