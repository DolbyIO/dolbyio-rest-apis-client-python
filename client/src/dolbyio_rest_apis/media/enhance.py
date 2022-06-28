"""
dolbyio_rest_apis.media.enhance
~~~~~~~~~~~~~~~

This module contains the functions to work with the Enhance APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.enhance_response import EnhanceJob

async def start(
        access_token: str,
        job_content: str,
    ) -> str or None:
    r"""
    Starts enhancing to improve your media.

    The input location for your source media file as well as the output location for the processed result are required.

    This is an asynchronous operation so you will receive a job_id where you can retrieve the results when enhancement is complete.

    There are additional optional parameters that can be provided to control and select the type of
    enhancements made. See the samples for some examples of what requests and responses look like.

    See: https://docs.dolby.io/media-apis/reference/media-enhance-post

    Args:
        access_token: Access token to use for authentication.
        job_content: Content of the job description as a JSON payload.
            You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-enhance-post

    Returns:
        The job identifier.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url='https://api.dolby.com/media/enhance',
            payload=job_content,
        )

    if 'job_id' in json_response:
        return json_response['job_id']

async def get_results(
        access_token: str,
        job_id: str,
    ) -> EnhanceJob:
    r"""
    Gets Enhance Results

    For a given job_id, this method will check if the processing task has completed and return the enhanced results.

    When the status is Success you'll be able to retrieve your result from the output location you provided in the original POST.

    See: https://docs.dolby.io/media-apis/reference/media-enhance-get

    Args:
        access_token: Access token to use for authentication.
        job_id: The job identifier.

    Returns:
        An :class:`EnhanceJob` object.

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
            url='https://api.dolby.com/media/enhance',
            params=params
        )

    return EnhanceJob(job_id, json_response)
