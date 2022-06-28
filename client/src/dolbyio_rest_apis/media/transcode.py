"""
dolbyio_rest_apis.media.transcode
~~~~~~~~~~~~~~~

This module contains the functions to work with the Transcode APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.transcode_response import TranscodeJob

async def start(
        access_token: str,
        job_content: str,
    ) -> str or None:
    r"""
    Start transcoding to modify the resolutions, bitrates, and formats for your media.

    The inputs location and outputs are required to identify the source material and target for results.

    This is an asynchronous operation so you will receive a job_id to use in calling GET /media/transcode to retrieve the job status.

    There are additional optional parameters that can be provided to further specify the desired output content types.

    See the samples for examples of transcode requests.

    See: https://docs.dolby.io/media-apis/reference/media-transcode-post

    Args:
        access_token: Access token to use for authentication.
        job_content: Content of the job description as a JSON payload.
            You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-transcode-post

    Returns:
        The job identifier.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url='https://api.dolby.com/media/transcode',
            payload=job_content,
        )

    if 'job_id' in json_response:
        return json_response['job_id']

async def get_results(
        access_token: str,
        job_id: str,
    ) -> TranscodeJob:
    r"""
    Gets Transcode Results.

    For a given job_id, this method will check if the transcoding task has completed and return transcoding results.

    See: https://docs.dolby.io/media-apis/reference/media-transcode-get

    Args:
        access_token: Access token to use for authentication.
        job_id: The job identifier.

    Returns:
        An :class:`TranscodeJob` object.

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
            url='https://api.dolby.com/media/transcode',
            params=params
        )

    return TranscodeJob(job_id, json_response)
