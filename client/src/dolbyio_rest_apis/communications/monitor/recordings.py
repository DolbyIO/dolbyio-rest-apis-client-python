"""
dolbyio_rest_apis.communications.monitor.recordings
~~~~~~~~~~~~~~~

This module contains the functions to work with the monitor API related to recordings.
"""

from deprecated import deprecated
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_monitor_url
from dolbyio_rest_apis.communications.monitor.models import GetRecordingsResponse, Recording, DolbyVoiceRecording
from typing import Any, List

async def get_recordings(
        access_token: str,
        tr_from: int=0,
        tr_to: int=9999999999999,
        maximum: int=100,
        start: str=None,
        perm: bool=False,
    ) -> GetRecordingsResponse:
    r"""
    Get recording details

    Get a list of the recorded conference metadata, such as duration or size of the recording.
    This API checks only the recordings that have ended during a specific time range.
    Recordings are indexed based on the ending time.

    See: https://docs.dolby.io/communications-apis/reference/get-recordings

    Args:
        access_token: Access token to use for authentication.
        tr_from: The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: The end of the time range (in milliseconds that have elapsed since epoch).
        maximum: The maximum number of displayed results.
            We recommend setting the proper value of this parameter to shorten the response time.
        start: When the results span multiple pages, use this option to navigate through pages.
            By default, only the max number of results is displayed. To see the next results,
            set the start parameter to the value of the next key returned in the previous response.
        perm: When set to true, the URL is replaced with a monitor API signed URL with unlimited validity.

    Returns:
        A :class:`GetRecordingsResponse` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/recordings'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': maximum,
        'perm': str(perm).lower(),
    }

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
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
        perm: bool=False,
    ) -> List[Recording]:
    r"""
    Get all recording details

    Get a list of all the recorded conference metadata, such as duration or size of the recording.
    This API checks only the recordings that have ended during a specific time range.
    Recordings are indexed based on the ending time.

    See: https://docs.dolby.io/communications-apis/reference/get-recordings

    Args:
        access_token: Access token to use for authentication.
        tr_from: The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.
        perm: When set to true, the URL is replaced with a monitor API signed URL with unlimited validity.

    Returns:
        A list of :class:`Recording` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/recordings'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
        'perm': str(perm).lower(),
    }

    recordings = []

    async with CommunicationsHttpContext() as http_context:
        elements: List[Any] = await http_context.requests_get_all(
            access_token=access_token,
            url=url,
            params=params,
            property_name='recordings',
            page_size=page_size
        )

    recordings: List[Recording] = []
    for element in elements:
        recording = Recording(element)
        recordings.append(recording)

    return recordings

async def get_recording(
        access_token: str,
        conference_id: str,
        tr_from: int=0,
        tr_to: int=9999999999999,
        page_size: int=100,
        perm: bool=False,
    ) -> GetRecordingsResponse:
    r"""
    Get the recording of a specific conference

    Get a list of the recorded conference metadata, such as duration or size of the recording.
    This API checks the recordings that have ended during a specific time range.
    Recordings are indexed based on the ending time.

    See: https://docs.dolby.io/communications-apis/reference/get-conference-recordings

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        tr_from: The beginning of the time range (in milliseconds that have elapsed since epoch).
        tr_to: The end of the time range (in milliseconds that have elapsed since epoch).
        page_size: (Optional) Number of elements to return per page.
        perm: When set to true, the URL is replaced with a monitor API signed URL with unlimited validity.

    Returns:
        A :class:`GetRecordingsResponse` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    url = f'{get_monitor_url()}/conferences/{conference_id}/recordings'

    params = {
        'from': tr_from,
        'to': tr_to,
        'max': page_size,
        'perm': str(perm).lower(),
    }

    recordings = []

    async with CommunicationsHttpContext() as http_context:
        elements: List[Any] = await http_context.requests_get_all(
            access_token=access_token,
            url=url,
            params=params,
            property_name='recordings',
            page_size=page_size
        )

    recordings: List[Recording] = []
    for element in elements:
        recording = Recording(element)
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

    url = f'{get_monitor_url()}/conferences/{conference_id}/recordings'

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_delete(
            access_token=access_token,
            url=url,
        )

async def get_dolby_voice_recordings(
        access_token: str,
        conference_id: str,
    ) -> DolbyVoiceRecording:
    r"""
    Get Dolby Voice audio recordings of a conference

    Get details of all Dolby Voice-based audio recordings, and associated split recordings,
    for a given conference and download the conference recording in the MP3 audio format.

    See: https://docs.dolby.io/communications-apis/reference/get-dolby-voice-audio-recordings

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Returns:
        A :class:`DolbyVoiceRecording` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    url = f'{get_monitor_url()}/conferences/{conference_id}/recordings/audio'

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url=url,
        )

    return DolbyVoiceRecording(json_response)

@deprecated(reason='This API is no longer applicable on the Dolby.io Communications APIs platform.')
async def download_mp4_recording(
        access_token: str,
        conference_id: str,
        file_path: str,
    ) -> None:
    r"""
    Download the conference recording in MP4 format

    Download the conference recording in the MP4 video format.
    For more information, see the [Recording](https://docs.dolby.io/communications-apis/docs/guides-recording-mechanisms) document.

    See: https://docs.dolby.io/communications-apis/reference/get-mp4-recording

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        file_path: Where to save the file.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    url = f'{get_monitor_url()}/conferences/{conference_id}/recordings/mp4'

    async with CommunicationsHttpContext() as http_context:
        await http_context.download(
            access_token=access_token,
            url=url,
            accept='video/mp4',
            file_path=file_path,
        )

@deprecated(reason='This API is no longer applicable on the Dolby.io Communications APIs platform.')
async def download_mp3_recording(
        access_token: str,
        conference_id: str,
        file_path: str,
    ) -> None:
    r"""
    Download the conference recording in MP3 format

    Download the conference recording in the MP3 audio format. This API is available only for non-Dolby Voice conferences.
    For more information, see the [Recording](https://docs.dolby.io/communications-apis/docs/guides-recording-mechanisms) document.

    See: https://docs.dolby.io/communications-apis/reference/get-mp3-recording

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        file_path: Where to save the file.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    url = f'{get_monitor_url()}/conferences/{conference_id}/recordings/mp3'

    async with CommunicationsHttpContext() as http_context:
        await http_context.download(
            access_token=access_token,
            url=url,
            accept='video/mpeg',
            file_path=file_path,
        )
