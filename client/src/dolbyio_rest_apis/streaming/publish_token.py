"""
dolbyio_rest_apis.streaming.publish_token
~~~~~~~~~~~~~~~

This module contains the functions to work with the Publish Token APIs.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_rts_url
from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.models.publish_token import PublishToken, UpdatePublishToken, CreatePublishToken, ActivePublishToken, DisablePublishTokenResponse

async def read(
        api_secret: str,
        token_id: int,
    ) -> PublishToken:
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token/{token_id}',
        )

    return PublishToken.from_dict(dict_data)

async def delete(
        api_secret: str,
        token_id: int,
    ) -> None:
    async with StreamingHttpContext() as http_context:
        await http_context.requests_delete(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token/{token_id}',
        )

async def update(
        api_secret: str,
        token_id: int,
        token: UpdatePublishToken,
    ) -> PublishToken:
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
    add_if_not_none(payload, 'subscribeRequiresAuth', token.subscribe_requires_auth)
    add_if_not_none(payload, 'record', token.record)
    add_if_not_none(payload, 'multisource', token.multisource)
    add_if_not_none(payload, 'enableThumbnails', token.enable_thumbnails)
    add_if_not_none(payload, 'displaySrtPassphrase', token.display_srt_passphrase)
    add_if_not_none(payload, 'lowLatencyRtmp', token.low_latency_rtmp)
    add_if_not_none(payload, 'clip', token.clip)
    if token.update_geo_cascade is not None:
        payload['updateGeoCascade'] = {
            'isEnabled': token.update_geo_cascade.is_enabled,
            'clusters': token.update_geo_cascade.clusters,
        }
    if token.update_restream is not None:
        payload['updateRestream'] = []
        for restream in token.update_restream:
            restream_obj = {
                'url': restream.url,
                'key': restream.key,
            }
            payload['updateRestream'].append(restream_obj)

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_put(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token/{token_id}',
            payload=payload,
        )

    return PublishToken.from_dict(dict_data)

async def list_tokens(
        api_secret: str,
        sort_by: str,
        page: int,
        items_on_page: int,
        is_descending: bool = False,
    ) -> list[PublishToken]:
    params = {
        'sortBy': sort_by,
        'page': str(page),
        'itemsOnPage': str(items_on_page),
        'isDescending': str(is_descending),
    }

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token/list',
            params=params,
        )

    tokens = []
    for token in dict_data:
        tokens.append(PublishToken.from_dict(token))
    return tokens

async def create(
        api_secret: str,
        token: CreatePublishToken,
    ) -> PublishToken:
    payload = {
        'label': token.label,
        'streams': [],
        'subscribeRequiresAuth': token.subscribe_requires_auth,
        'record': token.record,
        'multisource': token.multisource,
        'enableThumbnails': token.enable_thumbnails,
        'displaySrtPassphrase': token.display_srt_passphrase,
        'lowLatencyRtmp': token.low_latency_rtmp,
        'clip': token.clip,
        'restream': [],
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
    if not token.geo_cascade is None:
        payload['geoCascade'] = {
            'isEnabled': token.geo_cascade.is_enabled,
            'clusters': token.geo_cascade.clusters,
        }
    for restream in token.restream:
        payload['restream'] = {
            'url': restream.url,
            'key': restream.key,
        }

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_post(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token',
            payload=payload,
        )

    return PublishToken.from_dict(dict_data)

async def get_active_publish_token_id(
        api_secret: str,
        stream_id: str,
    ) -> ActivePublishToken:
    params = {
        'streamId': stream_id,
    }
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token/active',
            params=params,
        )

    return ActivePublishToken.from_dict(dict_data)

async def get_all_active_publish_token_id(
        api_secret: str,
    ) -> ActivePublishToken:
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token/active/all',
        )

    return ActivePublishToken.from_dict(dict_data)

async def disable(
        api_secret: str,
        token_ids: list[int],
    ) -> DisablePublishTokenResponse:
    payload = {
        'tokenIds': token_ids,
    }
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_patch(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/publish_token/disable',
            payload=payload,
        )

    return DisablePublishTokenResponse.from_dict(dict_data)
