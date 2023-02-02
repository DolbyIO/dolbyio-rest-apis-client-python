"""
dolbyio_rest_apis.streaming.subscribe_token
~~~~~~~~~~~~~~~

This module contains the functions to work with the Subscribe Token APIs.
"""

from typing import List
from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.internal.urls import SAPI_URL
from dolbyio_rest_apis.streaming.models.subscribe_token import SubscribeToken, UpdateSubscribeToken, CreateSubscribeToken

async def read(
        api_secret: str,
        token_id: int,
    ) -> SubscribeToken:
    async with StreamingHttpContext() as http_context:
        json_response = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/subscribe_token/{token_id}',
        )

    return SubscribeToken(json_response)

async def delete(
        api_secret: str,
        token_id: int,
    ) -> None:
    async with StreamingHttpContext() as http_context:
        await http_context.requests_delete(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/subscribe_token/{token_id}',
        )

async def update(
        api_secret: str,
        token_id: int,
        token: UpdateSubscribeToken,
    ) -> SubscribeToken:
    payload = {}
    add_if_not_none(payload, 'label', token.label)
    add_if_not_none(payload, 'refreshToken', token.refresh_token)
    add_if_not_none(payload, 'isActive', token.is_active)
    if token.add_token_streams is not None:
        payload['addTokenStreams'] = []
        for stream in token.add_token_streams:
            stream_obj = {
                'streamName': stream.stream_name,
            }
            add_if_not_none(stream_obj, 'isRegex', stream.is_regex)
            payload['addTokenStreams'].append(stream_obj)
    if token.remove_token_streams is not None:
        payload['removeTokenStreams'] = []
        for stream in token.remove_token_streams:
            stream_obj = {
                'streamName': stream.stream_name,
            }
            add_if_not_none(stream_obj, 'isRegex', stream.is_regex)
            payload['removeTokenStreams'].append(stream_obj)
    add_if_not_none(payload, 'updateAllowedOrigins', token.update_allowed_origins)
    add_if_not_none(payload, 'updateAllowedIpAddresses', token.update_allowed_ip_addresses)
    add_if_not_none(payload, 'updateBindIpsOnUsage', token.update_bind_ips_on_usage)
    add_if_not_none(payload, 'updateAllowedCountries', token.update_allowed_countries)
    add_if_not_none(payload, 'updateDeniedCountries', token.update_denied_countries)
    add_if_not_none(payload, 'updateOriginCluster', token.update_origin_cluster)
    async with StreamingHttpContext() as http_context:
        json_response = await http_context.requests_put(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/subscribe_token/{token_id}',
            payload=payload,
        )

    return SubscribeToken(json_response)

async def list_tokens(
        api_secret: str,
        sort_by: str,
        page: int,
        items_on_page: int,
        is_descending: bool,
    ) -> List[SubscribeToken]:
    params = {
        'sortBy': sort_by,
        'page': str(page),
        'itemsOnPage': str(items_on_page),
        'isDescending': str(is_descending),
    }

    async with StreamingHttpContext() as http_context:
        json_response = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/subscribe_token/list',
            params=params,
        )

    publish_tokens = []
    for token in json_response:
        publish_tokens.append(SubscribeToken(token))
    return publish_tokens

async def create(
        api_secret: str,
        token: CreateSubscribeToken,
    ) -> SubscribeToken:
    payload = {
        'label': token.label,
        'streams': [],
    }
    add_if_not_none(payload, 'expiresOn', token.expires_on)
    for stream in token.streams:
        stream_obj = {
            'streamName': stream.stream_name,
        }
        add_if_not_none(stream_obj, 'isRegex', stream.is_regex)
        payload['streams'].append(stream_obj)
    add_if_not_none(payload, 'allowedOrigins', token.allowed_origins)
    add_if_not_none(payload, 'allowedIpAddresses', token.allowed_ip_addresses)
    add_if_not_none(payload, 'bindIpsOnUsage', token.bind_ips_on_usage)
    add_if_not_none(payload, 'allowedCountries', token.allowed_countries)
    add_if_not_none(payload, 'deniedCountries', token.denied_countries)
    add_if_not_none(payload, 'originCluster', token.origin_cluster)

    async with StreamingHttpContext() as http_context:
        json_response = await http_context.requests_post(
            api_secret=api_secret,
            url=f'{SAPI_URL}/api/subscribe_token',
            payload=token,
        )

    return SubscribeToken(json_response)
