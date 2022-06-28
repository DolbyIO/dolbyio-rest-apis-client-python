"""
dolbyio_rest_apis.media.webhooks
~~~~~~~~~~~~~~~

This module contains the functions to work with the Platform Webhooks APIs.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.webhook import Webhook
from typing import Any, Dict

async def register_webhook(
        access_token: str,
        url: str,
        headers: Dict[str, Any]=None,
    ) -> str or None:
    r"""
    Registers a webhook that is triggered when a job completes.

    See: https://docs.dolby.io/media-apis/reference/media-webhook-post

    Args:
        access_token: Access token to use for authentication.
        url: The callback url that will be called when job execution completes.
        headers: (Optional) Headers to include in the webhook call.

    Returns:
        The webhook identifier.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    request_url = 'https://api.dolby.com/media/webhooks'

    payload = {
        'callback': {
            'url': url,
        }
    }
    add_if_not_none(payload['callback'], 'headers', headers)

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url=request_url,
            payload=payload,
        )

    if 'webhook_id' in json_response:
        return json_response['webhook_id']

async def update_webhook(
        access_token: str,
        webhook_id: str,
        url: str,
        headers: Dict[str, Any]=None,
    ):
    r"""
    Updates the previously registered webhook configuration.

    See: https://docs.dolby.io/media-apis/reference/media-webhook-put

    Args:
        access_token: Access token to use for authentication.
        webhook_id: Use the `webhook_id` returned from a previous GET, POST
            or PUT response to retrieve the webhook configuration.
        url: The callback url that will be called when job execution completes.
        headers: (Optional) Headers to include in the webhook call.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    request_url = 'https://api.dolby.com/media/webhooks'

    params = {
        'id': webhook_id
    }

    payload = {
        'callback': {
            'url': url,
        }
    }
    add_if_not_none(payload['callback'], 'headers', headers)

    async with MediaHttpContext() as http_context:
        await http_context.requests_put(
            access_token=access_token,
            url=request_url,
            params=params,
            payload=payload,
        )

async def retrieve_webhook(
        access_token: str,
        webhook_id: str,
    ) -> Webhook:
    r"""
    Retrieves the previously registered webhook configuration.

    See: https://docs.dolby.io/media-apis/reference/media-webhook-get

    Args:
        access_token: Access token to use for authentication.
        url: The callback url that will be called when job execution completes.
        headers: (Optional) Headers to include in the webhook call.

    Returns:
        A :class:`Webhook` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    params = {
        'id': webhook_id
    }

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url='https://api.dolby.com/media/webhooks',
            params=params,
        )

    return Webhook(json_response)

async def delete_webhook(
        access_token: str,
        webhook_id: str,
    ) -> str or None:
    r"""
    Deletes a previously registered webhook configuration.

    See: https://docs.dolby.io/media-apis/reference/media-webhook-delete

    Args:
        access_token: Access token to use for authentication.
        webhook_id: Use the `webhook_id` returned from a previous GET, POST
            or PUT response to retrieve the webhook configuration.

    Returns:
        The webhook identifier.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    params = {
        'id': webhook_id
    }

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_delete(
            access_token=access_token,
            url='https://api.dolby.com/media/webhooks',
            params=params,
        )

    if 'webhook_id' in json_response:
        return json_response['webhook_id']
