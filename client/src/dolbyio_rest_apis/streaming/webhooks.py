"""
dolbyio_rest_apis.streaming.webhooks
~~~~~~~~~~~~~~~

This module contains the functions to work with the Webhooks APIs.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_rts_url
from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.models.webhooks import CreateWebhook, UpdateWebhook, Webhook

async def read(
        api_secret: str,
        webhook_id: int,
    ) -> Webhook:
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/webhooks/{webhook_id}',
        )

    return Webhook.from_dict(dict_data)

async def delete(
        api_secret: str,
        webhook_id: int,
    ) -> None:
    async with StreamingHttpContext() as http_context:
        await http_context.requests_delete(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/webhooks/{webhook_id}',
        )

async def update(
        api_secret: str,
        webhook_id: int,
        webhook: UpdateWebhook,
    ) -> Webhook:
    payload = {}
    add_if_not_none(payload, 'url', webhook.url)
    add_if_not_none(payload, 'refreshSecret', webhook.refresh_secret)
    add_if_not_none(payload, 'isFeedHooks', webhook.is_feed_hooks)
    add_if_not_none(payload, 'isRecordingHooks', webhook.is_recording_hooks)
    add_if_not_none(payload, 'isThumbnailHooks', webhook.is_thumbnail_hooks)
    add_if_not_none(payload, 'isTranscoderHooks', webhook.is_transcoder_hooks)
    add_if_not_none(payload, 'isClipHooks', webhook.is_clip_hooks)

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_put(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/webhooks/{webhook_id}',
            payload=payload,
        )

    return Webhook.from_dict(dict_data)

async def list_webhooks(
        api_secret: str,
        starting_id: int,
        item_count: int = 10,
        is_descending: bool = False,
    ) -> list[Webhook]:
    params = {
        'startingId': str(starting_id),
        'item_count': str(item_count),
        'isDescending': str(is_descending),
    }

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/webhooks/list',
            params=params,
        )

    webhooks = []
    for webhook in dict_data:
        webhooks.append(Webhook.from_dict(webhook))
    return webhooks

async def create(
        api_secret: str,
        webhook: CreateWebhook,
    ) -> Webhook:
    payload = {
        'url': webhook.url,
        'isFeedHooks': webhook.is_feed_hooks,
        'isRecordingHooks': webhook.is_recording_hooks,
    }
    add_if_not_none(payload, 'isThumbnailHooks', webhook.is_thumbnail_hooks)
    add_if_not_none(payload, 'isTranscoderHooks', webhook.is_transcoder_hooks)
    add_if_not_none(payload, 'isClipHooks', webhook.is_clip_hooks)

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_post(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/webhooks',
            payload=payload,
        )

    return Webhook.from_dict(dict_data)
