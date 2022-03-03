"""
dolbyio_rest_apis.communications.monitor.webhooks
~~~~~~~~~~~~~~~

This module contains the functions to work with the monitor API related to webhooks.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_monitor_url
from dolbyio_rest_apis.communications.monitor.models import GetWebHookResponse, WebHook
from typing import Any, List

async def get_events(
        access_token: str,
        conference_id: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        maximum: int=100,
        start: str=None,
        filter_type: str=None,
    ) -> GetWebHookResponse:
    r"""
    Get a list of Webhook events sent, during a specific time range.
    The list includes associated endpoint response codes and headers.

    See: https://docs.dolby.io/communications-apis/reference/get-webhooks

    Args:
        access_token: Access token to use for authentication.
        conference_id: (Optional) Identifier of the conference.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        maximum: (Optional) The maximum number of displayed results.
            We recommend setting the proper value of this parameter to shorten the response time.
        start: (Optional) When the results span multiple pages, use this option to navigate through pages.
            By default, only the max number of results is displayed. To see the next results,
            set the start parameter to the value of the next key returned in the previous response.
        filter_type: (Optional) The Webhook event type or an expression of its type (for example `Recording.Live.InProgress` or `Rec.*`).
            The default value of the type parameter returns all types of Webhooks.

    Returns:
        A :class:`GetWebHookResponse` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/'
    if not conference_id is None:
        url += f'conferences/{conference_id}/'
    url += 'webhooks'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': maximum,
    }

    if not filter_type is None:
        params['type'] = filter_type
    if not start is None:
        params['start'] = start

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
            params=params,
        )

    return GetWebHookResponse(json_response)

async def get_all_events(
        access_token: str,
        conference_id: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
        filter_type: str=None,
    ) -> List[WebHook]:
    r"""
    Get a list of all Webhook events sent, during a specific time range.
    The list includes associated endpoint response codes and headers.

    See: https://docs.dolby.io/communications-apis/reference/get-webhooks

    Args:
        access_token: Access token to use for authentication.
        conference_id: (Optional) Identifier of the conference.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.
        filter_type: (Optional) The Webhook event type or an expression of its type (for example `Recording.Live.InProgress` or `Rec.*`).
            The default value of the type parameter returns all types of Webhooks.

    Returns:
        A list of :class:`WebHook` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/'
    if not conference_id is None:
        url += f'conferences/{conference_id}/'
    url += 'webhooks'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
    }

    if not filter_type is None:
        params['type'] = filter_type

    async with CommunicationsHttpContext() as http_context:
        elements: List[Any] = await http_context.requests_get_all(
            access_token=access_token,
            url=url,
            params=params,
            property_name='webhooks',
            page_size=page_size
        )

    webhooks: List[WebHook] = []
    for element in elements:
        webhook = WebHook(element)
        webhooks.append(webhook)

    return webhooks
