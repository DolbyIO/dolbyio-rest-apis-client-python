"""
dolbyio_rest_apis.communications.monitor.conferences
~~~~~~~~~~~~~~~

This module contains the functions to work with the monitor API related to conferences.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_monitor_url
from dolbyio_rest_apis.communications.monitor.models import GetConferencesResponse, ConferenceSummary, ConferenceStatistics, ConferenceParticipants, ConferenceParticipant
from typing import Any, Dict, List

async def get_conferences(
        access_token: str,
        tr_from: int=0,
        tr_to: int=9999999999999,
        maximum: int=100,
        start: str=None,
        filter_alias: str=None,
        active: bool=False,
        external_id: str=None,
        live_stats: bool=False,
    ) -> GetConferencesResponse:
    r"""
    Get a list of conferences.

    Get a list of conferences that were started in a specific time range, including ongoing conferences.

    Note: Only terminated conferences include a complete summary.
    The summary of ongoing conferences includes the following fields in the response:
    `confId`, `alias`, `region`, `dolbyVoice`, `start`, `live`, `owner`.

    See: https://docs.dolby.io/communications-apis/reference/get-conferences

    Args:
        access_token: Access token to use for authentication.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        maximum: (Optional) The maximum number of displayed results.
            We recommend setting the proper value of this parameter to shorten the response time.
        start: (Optional) When the results span multiple pages, use this option to navigate through pages.
            By default, only the max number of results is displayed. To see the next results,
            set the start parameter to the value of the next key returned in the previous response.
        filter_alias: (Optional) Search conferences using Alias. Use regular expression to search for conferences with similar aliases.
            For example:
            - Use `foobar` to get all conferences with alias foobar.
            - Use `.*foobar` to get all conferences with alias ending with foobar.
            - Use `foobar.*` to get all conferences with alias starting with foobar
            - Use `.*foobar.*` to get all conferences with alias containing foobar.
            - Use `.*2019.*|.*2020.*` to get all conferences with alias containing either 2019 or 2020.
        active: (Optional) Search for ongoing references (`true`) or all conferences (`false`).
        external_id: (Optional) The external ID of the participant who created the conference.
        live_stats: (Optional) For live conferences, the number of `user`, `listener`, and `pstn` participants.

    Returns:
        A :class:`GetConferencesResponse` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/conferences'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': maximum,
        'active': str(active),
        'livestats': str(live_stats),
    }

    if not start is None:
        params['start'] = start
    if not filter_alias is None:
        params['alias'] = filter_alias
    if not external_id is None:
        params['exid'] = external_id

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
            params=params,
        )

    return GetConferencesResponse(json_response)

async def get_all_conferences(
        access_token: str,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
        filter_alias: str=None,
        active: bool=False,
        external_id: str=None,
        live_stats: bool=False,
    ) -> List[ConferenceSummary]:
    r"""
    Get a list of all conferences.

    Get a list of all conferences that were started in a specific time range, including ongoing conferences.

    Note: Only terminated conferences include a complete summary.
    The summary of ongoing conferences includes the following fields in the response:
    `confId`, `alias`, `region`, `dolbyVoice`, `start`, `live`, `owner`.

    See: https://docs.dolby.io/communications-apis/reference/get-conferences

    Args:
        access_token: Access token to use for authentication.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.
        filter_alias: (Optional) Search conferences using Alias. Use regular expression to search for conferences with similar aliases.
            For example:
            - Use `foobar` to get all conferences with alias foobar.
            - Use `.*foobar` to get all conferences with alias ending with foobar.
            - Use `foobar.*` to get all conferences with alias starting with foobar
            - Use `.*foobar.*` to get all conferences with alias containing foobar.
            - Use `.*2019.*|.*2020.*` to get all conferences with alias containing either 2019 or 2020.
        active: (Optional) Search for ongoing references (`true`) or all conferences (`false`).
        external_id: (Optional) The external ID of the participant who created the conference.
        live_stats: (Optional) For live conferences, the number of `user`, `listener`, and `pstn` participants.

    Returns:
        A list of :class:`Conference` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/conferences'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
        'active': str(active),
        'livestats': str(live_stats),
    }

    if not filter_alias is None:
        params['alias'] = filter_alias
    if not external_id is None:
        params['exid'] = external_id

    async with CommunicationsHttpContext() as http_context:
        elements: List[Any] = await http_context.requests_get_all(
            access_token=access_token,
            url=url,
            params=params,
            property_name='conferences',
            page_size=page_size
        )

    conferences: List[ConferenceSummary] = []
    for element in elements:
        conference = ConferenceSummary(element)
        conferences.append(conference)

    return conferences

async def get_conference(
        access_token: str,
        conference_id: str,
        live_stats: bool=False,
    ) -> ConferenceSummary:
    r"""
    Get a summary of a conference.

    Note: Only terminated conferences include a complete summary.
    The summary of ongoing conferences includes the following fields in the response:
    `confId`, `alias`, `region`, `dolbyVoice`, `start`, `live`, `owner`.

    See: https://docs.dolby.io/communications-apis/reference/get-conference-summary

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        live_stats: (Optional) For live conferences, the number of `user`, `listener`, and `pstn` participants.

    Returns:
        A :class:`ConferenceSummary` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    url = f'{get_monitor_url()}/conferences/{conference_id}'

    params = {
        'livestats': str(live_stats),
    }

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
            params=params,
        )

    return ConferenceSummary(json_response)

async def get_conference_statistics(
        access_token: str,
        conference_id: str,
    ) -> ConferenceStatistics:
    r"""
    Get a conference statistics.

    Get statistics of a terminated conference.
    The statistics include the maximum number of participants present during a conference
    and the maximum number of the transmitted and received packets, bytes, and streams.

    Note: The statistics are available only for terminated conferences.

    See: https://docs.dolby.io/communications-apis/reference/get-conference-statistics

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        live_stats: For live conferences, the number of `user`, `listener`, and `pstn` participants.

    Returns:
        A :class:`ConferenceStatistics` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    url = f'{get_monitor_url()}/conferences/{conference_id}/statistics'

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
        )

    return ConferenceStatistics(json_response)

async def get_conference_participants(
        access_token: str,
        conference_id: str,
        participant_type: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        maximum: int=100,
        start: str=None,
    ) -> ConferenceParticipants:
    r"""
    Get information about conference participants.

    Get statistics and connection details of all participants in a conference.
    Optionally limit the search result with a specific time range.

    See: https://docs.dolby.io/communications-apis/reference/get-info-conference-participants

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        participant_type: (Optional) The conference participant type.
            - `user` - a participant who can send and receive video/audio stream to/from the conference.
            - `listener` - a participant who can only receive video/audio stream from the conference.
            - `pstn` - a participant who connected to the conference using PSTN (telephony network).
            - `mixer` - an internal type indicating a mixer connection to the conference.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        maximum: (Optional) The maximum number of displayed results.
            We recommend setting the proper value of this parameter to shorten the response time.
        start: (Optional) When the results span multiple pages, use this option to navigate through pages.
            By default, only the max number of results is displayed. To see the next results,
            set the start parameter to the value of the next key returned in the previous response.

    Returns:
        A :class:`ConferenceParticipants` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/conferences/{conference_id}/participants'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': maximum,
    }
    if not participant_type is None:
        params['type'] = participant_type
    if not start is None:
        params['start'] = start

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
            params=params,
        )

        return ConferenceParticipants(json_response)

async def get_all_conference_participants(
        access_token: str,
        conference_id: str,
        participant_type: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
    ) -> Dict[str, ConferenceParticipant]:
    r"""
    Get information about all conference participants.

    Get statistics and connection details of all participants in a conference.
    Optionally limit the search result with a specific time range.

    See: https://docs.dolby.io/communications-apis/reference/get-info-conference-participants

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        participant_type: (Optional) The conference participant type.
            - `user` - a participant who can send and receive video/audio stream to/from the conference.
            - `listener` - a participant who can only receive video/audio stream from the conference.
            - `pstn` - a participant who connected to the conference using PSTN (telephony network).
            - `mixer` - an internal type indicating a mixer connection to the conference.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.

    Returns:
        A list of :class:`ConferenceParticipant` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/conferences/{conference_id}/participants'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
    }
    if not participant_type is None:
        params['type'] = participant_type

    participants: Dict[str, ConferenceParticipant] = {}

    async with CommunicationsHttpContext() as http_context:
        while True:
            json_response = await http_context.requests_get(
                access_token=access_token,
                url=url,
                params=params,
            )

            if 'participants' in json_response:
                sub_result = json_response['participants']
                for participant_id in sub_result:
                    participant = ConferenceParticipant(participant_id, sub_result[participant_id])
                    participants[participant.user_id] = participant

                if len(sub_result) < page_size:
                    break

            if not 'next' in json_response:
                break

            params['start'] = json_response['next']
            if params['start'] is None or params['start'] == '':
                break

    return participants

async def get_conference_participant(
        access_token: str,
        conference_id: str,
        participant_id: str,
        participant_type: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        maximum: int=100,
        start: str=None,
    ) -> ConferenceParticipant:
    r"""
    Get information about a specific conference participant.

    Gets the statistics and connection details of a conference participant, during a specific time range.

    See: https://docs.dolby.io/communications-apis/reference/get-info-conference-participant

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        participant_id: Identifier of the participant.
        participant_type: (Optional) The conference participant type.
            - `user` - a participant who can send and receive video/audio stream to/from the conference.
            - `listener` - a participant who can only receive video/audio stream from the conference.
            - `pstn` - a participant who connected to the conference using PSTN (telephony network).
            - `mixer` - an internal type indicating a mixer connection to the conference.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        maximum: (Optional) The maximum number of displayed results.
            We recommend setting the proper value of this parameter to shorten the response time.
        start: (Optional) When the results span multiple pages, use this option to navigate through pages.
            By default, only the max number of results is displayed. To see the next results,
            set the start parameter to the value of the next key returned in the previous response.

    Returns:
        A :class:`ConferenceParticipant` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/conferences/{conference_id}/participants/{participant_id}'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': maximum,
    }
    if not participant_type is None:
        params['type'] = participant_type
    if not start is None:
        params['start'] = start

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
            params=params,
        )

        participants = ConferenceParticipants(json_response)
        return participants[participant_id]
