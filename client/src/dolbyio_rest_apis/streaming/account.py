"""
dolbyio_rest_apis.streaming.account
~~~~~~~~~~~~~~~

This module contains the functions to work with the Account APIs.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.core.urls import get_rts_url
from dolbyio_rest_apis.streaming.internal.http_context import StreamingHttpContext
from dolbyio_rest_apis.streaming.models.account import AccountGeoCascade, AccountGeoRestrictions

async def read_geo_cascade(
        api_secret: str,
    ) -> AccountGeoCascade:
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/account/geo_cascade',
        )

    return AccountGeoCascade.from_dict(dict_data)

async def update_geo_cascade(
        api_secret: str,
        geo_cascade: AccountGeoCascade,
    ) -> AccountGeoCascade:
    payload = {
        'isEnabled': geo_cascade.is_enabled,
    }
    add_if_not_none(payload, 'clusters', geo_cascade.clusters)

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_put(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/account/geo_cascade',
            payload=payload,
        )

    return AccountGeoCascade.from_dict(dict_data)

async def read_geo_restrictions(
        api_secret: str,
    ) -> AccountGeoRestrictions:
    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_get(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/geo/account',
        )

    return AccountGeoRestrictions.from_dict(dict_data)

async def update_geo_restrictions(
        api_secret: str,
        geo_restrictions: AccountGeoRestrictions,
    ) -> AccountGeoRestrictions:
    payload = {}
    add_if_not_none(payload, 'allowedCountries', geo_restrictions.allowed_countries)
    add_if_not_none(payload, 'deniedCountries', geo_restrictions.denied_countries)

    async with StreamingHttpContext() as http_context:
        dict_data = await http_context.requests_post(
            api_secret=api_secret,
            url=f'{get_rts_url()}/api/geo/account',
            payload=payload,
        )

    return AccountGeoRestrictions.from_dict(dict_data)
