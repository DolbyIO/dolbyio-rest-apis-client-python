"""
dolbyio_rest_apis.communications.monitor.recordings
~~~~~~~~~~~~~~~

This module contains the functions to work with the monitor API related to recordings.
"""

from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.monitor.models import GetConferenceRecordingsResponse
from dolbyio_rest_apis.communications.monitor.models import GetRecordingsResponse, ConferenceRecording
from dolbyio_rest_apis.core.urls import get_comms_monitor_url_v2
from typing import Any, List

async def get_recordings(
        access_token: str,
        region: str=None,
        media_type: str=None,
        recording_type: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
        start: str=None,
    ) -> GetRecordingsResponse:
    r"""
    Gets a list of the recorded conference metadata, such as duration or size of the recording.
    This API checks only the recordings that have ended during a specific time range.
    Recordings are indexed based on the ending time.

    This API returns presigned URLs for secure download of the recording files.
    The URL returned in the response is an AWS S3 presigned URL with a validity of ten minutes.

    See: https://docs.dolby.io/communications-apis/reference/get-recordings

    Args:
        access_token: Access token to use for authentication.
        region: (Optional) The region code in which the mix recording took place.
        media_type: (Optional) The media type of the recordings to return, 'audio/mpeg' or 'video/mp4'.
        recording_type: (Optional) The type of the recordings to return, 'mix' or 'participant'.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.
        start: (Optional) When the results span multiple pages, use this option to navigate through pages.
            By default, only the max number of results is displayed. To see the next results,
            set the start parameter to the value of the next key returned in the previous response.

    Returns:
        A :class:`GetRecordingsV2Response` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_monitor_url_v2()}/recordings'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
    }

    if not region is None:
        params['region'] = region
    if not media_type is None:
        params['mediaType'] = media_type
    if not recording_type is None:
        params['type'] = recording_type
    if not start is None:
        params['start'] = start

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
            params=params,
        )

    return GetRecordingsResponse(json_response)

async def get_all_recordings(
        access_token: str,
        region: str=None,
        media_type: str=None,
        recording_type: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
    ) -> List[ConferenceRecording]:
    r"""
    Gets a list of all the recorded conference metadata, such as duration or size of the recording.
    This API checks only the recordings that have ended during a specific time range.
    Recordings are indexed based on the ending time.

    This API returns presigned URLs for secure download of the recording files.
    The URL returned in the response is an AWS S3 presigned URL with a validity of ten minutes.

    See: https://docs.dolby.io/communications-apis/reference/get-recordings

    Args:
        access_token: Access token to use for authentication.
        region: (Optional) The region code in which the mix recording took place.
        media_type: (Optional) The media type of the recordings to return, 'audio/mpeg' or 'video/mp4'.
        recording_type: (Optional) The type of the recordings to return, 'mix' or 'participant'.
        tr_from: (Optional) The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.

    Returns:
        A list of :class:`ConferenceRecording` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_monitor_url_v2()}/recordings'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
    }

    if not region is None:
        params['region'] = region
    if not media_type is None:
        params['mediaType'] = media_type
    if not recording_type is None:
        params['type'] = recording_type

    recordings = []

    async with CommunicationsHttpContext() as http_context:
        elements: List[Any] = await http_context.requests_get_all(
            access_token=access_token,
            url=url,
            params=params,
            property_name='recordings',
            page_size=page_size
        )

    recordings: List[ConferenceRecording] = []
    for element in elements:
        recording = ConferenceRecording(element)
        recordings.append(recording)

    return recordings

async def get_conference_recordings(
        access_token: str,
        conference_id: str,
        media_type: str=None,
        recording_type: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
        start: str=None,
    ) -> GetConferenceRecordingsResponse:
    r"""
    Gets a list of the recorded conference metadata, such as duration or size of the recording.

    This API checks only the recordings that have ended during a specific time range.
    Recordings are indexed based on the ending time.

    This API returns presigned URLs for secure download of the recording files.
    The URL returned in the response is an AWS S3 presigned URL with a validity of ten minutes.

    See: https://docs.dolby.io/communications-apis/reference/get-conference-recordings

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        media_type: (Optional) The media type of the recordings to return, 'audio/mpeg' or 'video/mp4'.
        recording_type: (Optional) The type of the recordings to return, 'mix' or 'participant'.
        tr_from:(Optional)  The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.

    Returns:
        A :class:`GetConferenceRecordingsResponse` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_monitor_url_v2()}/conferences/{conference_id}/recordings'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
    }

    if not media_type is None:
        params['mediaType'] = media_type
    if not recording_type is None:
        params['type'] = recording_type
    if not start is None:
        params['start'] = start

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
            params=params,
        )

    return GetConferenceRecordingsResponse(json_response)

async def get_all_conference_recordings(
        access_token: str,
        conference_id: str,
        media_type: str=None,
        recording_type: str=None,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
    ) -> List[ConferenceRecording]:
    r"""
    Gets a list of all the recorded conference metadata, such as duration or size of the recording.

    This API checks only the recordings that have ended during a specific time range.
    Recordings are indexed based on the ending time.

    This API returns presigned URLs for secure download of the recording files.
    The URL returned in the response is an AWS S3 presigned URL with a validity of ten minutes.

    See: https://docs.dolby.io/communications-apis/reference/get-conference-recordings

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        media_type: (Optional) The media type of the recordings to return, 'audio/mpeg' or 'video/mp4'.
        recording_type: (Optional) The type of the recordings to return, 'mix' or 'participant'.
        tr_from:(Optional)  The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: (Optional) The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.

    Returns:
        A list of :class:`ConferenceRecording` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_monitor_url_v2()}/conferences/{conference_id}/recordings'

    params = {
        'from': tr_from,
        'to': tr_to,
    }

    if not media_type is None:
        params['mediaType'] = media_type
    if not recording_type is None:
        params['type'] = recording_type

    recordings = []

    async with CommunicationsHttpContext() as http_context:
        elements: List[Any] = await http_context.requests_get_all(
            access_token=access_token,
            url=url,
            params=params,
            property_name='recordings',
            page_size=page_size
        )

    recordings: List[ConferenceRecording] = []
    for element in elements:
        recording = ConferenceRecording(element)
        recordings.append(recording)

    return recordings

async def delete_recording(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Delete recordings

    Delete all recording data related to a specific conference.

    Warning: After deleting the recording, it is not possible to restore the recording data.

    See: https://docs.dolby.io/communications-apis/reference/delete-conference-recordings

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_comms_monitor_url_v2()}/conferences/{conference_id}/recordings'

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_delete(
            access_token=access_token,
            url=url,
        )
