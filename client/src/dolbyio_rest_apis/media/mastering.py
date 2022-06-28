"""
dolbyio_rest_apis.media.transcode
~~~~~~~~~~~~~~~

This module contains the functions to work with the Transcode APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.mastering_response import MasteringPreviewJob, MasteringJob

async def start_preview(
        access_token: str,
        job_content: str,
    ) -> str or None:
    r"""
    Starts mastering preview to improve your music.

    The inputs location for your source media file as well as the outputs locations for the processed media files are required.

    A preset applies dynamic EQ processing to shape your music to match a desired sound.
    There are also additional optional parameters that can be provided to control the mastering output.

    A segment object specifying preview start may optionally be provided.

    This is an asynchronous operation. You receive a job_id that you use to retrieve the results when the mastering is complete.

    To learn more, see the example requests and responses.

    See: https://docs.dolby.io/media-apis/reference/media-music-mastering-preview-post

    Args:
        access_token: Access token to use for authentication.
        job_content: Content of the job description as a JSON payload.
            You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-music-mastering-preview-post

    Returns:
        The job identifier.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url='https://api.dolby.com/media/master/preview',
            payload=job_content,
        )

    if 'job_id' in json_response:
        return json_response['job_id']

async def get_preview_results(
        access_token: str,
        job_id: str,
    ) -> MasteringPreviewJob:
    r"""
    Gets Mastering Preview Results

    For a given job_id, this method will check if the mastering task has completed.
    When the status is Success you'll be able to retrieve your results from the outputs locations you provided in the original POST.

    See: https://docs.dolby.io/media-apis/reference/media-music-mastering-preview-get

    Args:
        access_token: Access token to use for authentication.
        job_id: The job identifier.

    Returns:
        An :class:`MasteringPreviewJob` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    params = {
        'job_id': job_id
    }

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url='https://api.dolby.com/media/master/preview',
            params=params
        )

    return MasteringPreviewJob(job_id, json_response)

async def start(
        access_token: str,
        job_content: str,
    ) -> str or None:
    r"""
    Starts mastering to improve your music.

    The inputs location for your source media file as well as the outputs location for the processed media file are required.

    A preset applies dynamic EQ processing to shape your music to match a desired sound.
    There are also additional optional parameters that can be provided to control the mastering output.

    This is an asynchronous operation. You receive a job_id that you use to retrieve the results when the mastering is complete.

    To learn more, see the example requests and responses.

    See: https://docs.dolby.io/media-apis/reference/media-music-mastering-post

    Args:
        access_token: Access token to use for authentication.
        job_content: Content of the job description as a JSON payload.
            You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-music-mastering-post

    Returns:
        The job identifier.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url='https://api.dolby.com/media/master',
            payload=job_content,
        )

    if 'job_id' in json_response:
        return json_response['job_id']

async def get_results(
        access_token: str,
        job_id: str,
    ) -> MasteringJob:
    r"""
    Gets Mastering Results

    For a given job_id, this method will check if the mastering task has completed.
    When the status is Success you'll be able to retrieve your results from the outputs locations you provided in the original POST.

    See: https://docs.dolby.io/media-apis/reference/media-music-mastering-get

    Args:
        access_token: Access token to use for authentication.
        job_id: The job identifier.

    Returns:
        An :class:`MasteringJob` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    params = {
        'job_id': job_id
    }

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_get(
            access_token=access_token,
            url='https://api.dolby.com/media/master',
            params=params
        )

    return MasteringJob(job_id, json_response)
