"""
dolbyio_rest_apis.streaming.cluster
~~~~~~~~~~~~~~~

This module contains the functions to work with the Cluster APIs.
"""

from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.internal.urls import SAPI_URL
from dolbyio_rest_apis.streaming.models.cluster import ClusterResponse

async def read(
        api_secret: str,
    ) -> ClusterResponse:
    async with StreamingHttpContext() as http_context:
        json_response = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/cluster',
        )

    return ClusterResponse(json_response)

async def update(
        api_secret: str,
        default_cluster: str,
    ) -> ClusterResponse:
    payload = {
        'defaultCluster': default_cluster,
    }

    async with StreamingHttpContext() as http_context:
        json_response = await http_context.requests_put(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/cluster',
            payload=payload,
        )

    return ClusterResponse(json_response)
