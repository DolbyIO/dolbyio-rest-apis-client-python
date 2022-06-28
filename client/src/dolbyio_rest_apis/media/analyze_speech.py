"""
dolbyio_rest_apis.media.analyze_speech
~~~~~~~~~~~~~~~

This module contains the functions to work with the Speech Analytics APIs.
"""

from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.analyze_speech_response import AnalyzeSpeechJob

async def start(
        access_token: str,
        job_content: str,
    ) -> str or None:
    r"""
    Starts analyzing to learn about speech in your media.

    The `input` location of your source media file and `output` location of your Analyze JSON results file are required.

    This is an asynchronous operation so you will receive a `job_id` to be used to get the job status and result.

    See: https://docs.dolby.io/media-apis/reference/media-analyze-speech-post

    Beta API
    This API is being made available as an early preview.
    If you have feedback on how you'd like to use the API please reach out to share your feedback with our team.
    https://dolby.io/contact

    Args:
        access_token: Access token to use for authentication.
        job_content: Content of the job description as a JSON payload.
            You can find the definition at this URL: https://docs.dolby.io/media-apis/reference/media-analyze-speech-post

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
            url='https://api.dolby.com/media/analyze/speech',
            payload=job_content,
        )

    if 'job_id' in json_response:
        return json_response['job_id']

async def get_results(
        access_token: str,
        job_id: str,
    ) -> AnalyzeSpeechJob:
    r"""
    Gets Speech Analytics Status.

    For a given job_id, this method will check if the processing task has completed.

    See: https://docs.dolby.io/media-apis/reference/media-analyze-speech-get

    Args:
        access_token: Access token to use for authentication.
        job_id: The job identifier.

    Returns:
        A :class:`AnalyzeSpeechJob` object.

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
            url='https://api.dolby.com/media/analyze/speech',
            params=params
        )

    return AnalyzeSpeechJob(job_id, json_response)
