"""
dolbyio_rest_apis.streaming.cluster
~~~~~~~~~~~~~~~

This module contains the functions to work with the Cluster APIs.
"""

from dolbyio_rest_apis.core.urls import get_rts_url
from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.models.cluster import ClusterResponse

async def read(
        api_secret: str,
    ) -> ClusterResponse:
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/cluster',
        )

    return ClusterResponse.from_dict(dict_data)

async def update(
        api_secret: str,
        default_cluster: str,
    ) -> ClusterResponse:
    payload = {
        'defaultCluster': default_cluster,
    }

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_put(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/cluster',
            payload=payload,
        )

    return ClusterResponse.from_dict(dict_data)
