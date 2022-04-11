"""
dolbyio_rest_apis.media.jobs
~~~~~~~~~~~~~~~

This module contains the functions to work with the Jobs APIs.
"""

from dolbyio_rest_apis.core.helpers import add_if_not_none
from dolbyio_rest_apis.media.internal.http_context import MediaHttpContext
from dolbyio_rest_apis.media.models.jobs_response import JobsResponse, Job
from typing import List

async def _list_jobs(
        http_context: MediaHttpContext,
        api_key: str,
        submitted_after: str=None,
        submitted_before: str=None,
        status: str=None,
        next_token: str=None,
    ) -> JobsResponse:
    params = { }
    add_if_not_none(params, 'submitted_after', submitted_after)
    add_if_not_none(params, 'submitted_before', submitted_before)
    add_if_not_none(params, 'status', status)
    add_if_not_none(params, 'next_token', next_token)

    json_response = await http_context.requests_get(
        api_key=api_key,
        url='https://api.dolby.com/media/jobs',
        params=params
    )

    return JobsResponse(json_response)

async def list_jobs(
        api_key: str,
        submitted_after: str=None,
        submitted_before: str=None,
        status: str=None,
        next_token: str=None,
    ) -> JobsResponse:
    r"""
    Query Media Jobs.

    List of jobs previously submitted, up to the last 31 days.

    See: https://docs.dolby.io/media-apis/reference/media-jobs-get

    Args:
        api_key: Your Dolby.io Media API Key.
        submitted_after: (Optional) Query jobs that were submitted at or after the specified date and time (inclusive).
        submitted_before: (Optional) Query jobs that were submitted at or before the specified date and time (inclusive).
            The `submitted_before` must be the same or later than `submitted_after`.
        status: (Optional) Query jobs that have the specified status.
        next_token: (Optional) Used when querying the next page of jobs. Specify the `next_token` that was returned in the previous call.

    Returns:
        A :class:`JobsResponse` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    async with MediaHttpContext() as http_context:
        json_response = await _list_jobs(
            http_context=http_context,
            api_key=api_key,
            submitted_after=submitted_after,
            submitted_before=submitted_before,
            status=status,
            next_token=next_token,
        )

    return JobsResponse(json_response)

async def list_all_jobs(
        api_key: str,
        submitted_after: str=None,
        submitted_before: str=None,
        status: str=None,
    ) -> JobsResponse:
    r"""
    Query Media Jobs.

    List of all jobs previously submitted, up to the last 31 days.

    See: https://docs.dolby.io/media-apis/reference/media-jobs-get

    Args:
        api_key: Your Dolby.io Media API Key.
        submitted_after: (Optional) Query jobs that were submitted at or after the specified date and time (inclusive).
        submitted_before: (Optional) Query jobs that were submitted at or before the specified date and time (inclusive).
            The `submitted_before` must be the same or later than `submitted_after`.
        status: (Optional) Query jobs that have the specified status.

    Returns:
        A list of :class:`Job` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    jobs: List[Job] = []

    async with MediaHttpContext() as http_context:
        next_token = None
        while True:
            page: JobsResponse = _list_jobs(
                http_context=http_context,
                api_key=api_key,
                submitted_after=submitted_after,
                submitted_before=submitted_before,
                status=status,
                next_token=next_token,
            )

            next_token = page.next_token
            for job in page.jobs:
                jobs.append(job)

            if page.next_token is None or page.next_token == '':
                break

    return jobs

async def cancel(
        api_key: str,
        job_id: str,
    ) -> None:
    r"""
    Requests cancellation of a previously submitted job.

    See: https://docs.dolby.io/media-apis/reference/media-jobs-cancel-post

    Args:
        api_key: Your Dolby.io Media API Key.
        job_id: Identifier of the job to cancel.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """
    params = {
        'job_id': job_id,
    }

    async with MediaHttpContext() as http_context:
        await http_context.requests_post(
            api_key=api_key,
            url='https://api.dolby.com/media/jobs/cancel',
            params=params,
        )
