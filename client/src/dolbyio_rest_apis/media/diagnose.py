"""
dolbyio_rest_apis.media.diagnose
~~~~~~~~~~~~~~~

This module contains the functions to work with the Diagnose APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.diagnose_response import DiagnoseJob

async def start(
        access_token: str,
        job_content: str,
    ) -> str or None:
    r"""
    Starts Diagnosing.

    The Dolby.io Media Analyze Audio Diagnose API provides a quick diagnosis for discovering audio quality issues with your media.

    See: https://docs.dolby.io/media-apis/reference/media-diagnose-post

    Beta API
    This API is being made available as an early preview.
    If you have feedback on how you'd like to use the API please reach out to share your feedback with our team.
    https://dolby.io/contact

    Args:
        access_token: Access token to use for authentication.
        job_content: Content of the job description as a JSON payload.
            You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-diagnose-post

    Returns:
        The job identifier.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    print('''Beta API
    This API is being made available as an early preview.
    If you have feedback on how you\'d like to use the API please reach out to share your feedback with our team.
    https://dolby.io/contact''')

    async with MediaHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url='https://api.dolby.com/media/diagnose',
            payload=job_content,
        )

    if 'job_id' in json_response:
        return json_response['job_id']

async def get_results(
        access_token: str,
        job_id: str,
    ) -> DiagnoseJob:
    r"""
    Gets Enhance Results

    For a given job_id, this method will check if the processing task has completed and return the enhanced results.

    When the status is Success you'll be able to retrieve your result from the output location you provided in the original POST.

    See: https://docs.dolby.io/media-apis/reference/media-diagnose-get

    Beta API
    This API is being made available as an early preview.
    If you have feedback on how you'd like to use the API please reach out to share your feedback with our team.
    https://dolby.io/contact

    Args:
        access_token: Access token to use for authentication.
        job_id: The job identifier.

    Returns:
        An :class:`DiagnoseJob` object.

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
            url='https://api.dolby.com/media/diagnose',
            params=params
        )

    return DiagnoseJob(job_id, json_response)
