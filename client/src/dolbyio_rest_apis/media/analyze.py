"""
dolbyio_rest_apis.media.analyze
~~~~~~~~~~~~~~~

This module contains the functions to work with the Analyze APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.analyze_response import AnalyzeJobResponse

async def start(
        access_token: str,
        job_content: str,
    ) -> str or None:
    r"""
    Starts analyzing to learn about your media.

    The `input` location of your source media file and `output` location of your Analyze JSON results file are required.

    This is an asynchronous operation so you will receive a `job_id` to be used to get the job status and result.

    There are additional optional parameters that can be provided to identify the type of content
    and additional loudness or validation requirements.
    See the samples for examples of what requests and responses look like.

    See: https://docs.dolby.io/media-apis/reference/media-analyze-post

    Beta API

    This API is being made available as an early preview.
    If you have feedback on how you'd like to use the API please reach out to share your feedback with our team.
    https://dolby.io/contact

    Content Length

    Media content with duration less than 2 seconds will not be processed. The API will return an ERROR in this case.

    Args:
        access_token: Access token to use for authentication.
        job_content: Content of the job description as a JSON payload.
            You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-analyze-post

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
            url='https://api.dolby.com/media/analyze',
            payload=job_content,
        )

    if 'job_id' in json_response:
        return json_response['job_id']

async def get_results(
        access_token: str,
        job_id: str,
    ) -> AnalyzeJobResponse:
    r"""
    Gets Analyze Status.

    For a given job_id, this method will check the job status.

    See: https://docs.dolby.io/media-apis/reference/media-analyze-get

    Args:
        access_token: Access token to use for authentication.
        job_id: The job identifier.

    Returns:
        A :class:`AnalyzeJobResponse` object.

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
            url='https://api.dolby.com/media/analyze',
            params=params
        )

    return AnalyzeJobResponse(job_id, json_response)
