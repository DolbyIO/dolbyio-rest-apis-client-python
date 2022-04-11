"""
dolbyio_rest_apis.media.models.jobs_response
~~~~~~~~~~~~~~~

This module contains the Jobs Response model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default, in_and_not_none
from .paged_response import PagedResponse

class JobsResponse(PagedResponse):
    r"""Representation of a jobs response."""

    def __init__(self, dictionary: dict):
        PagedResponse.__init__(self, dictionary)

        self.jobs = []
        if in_and_not_none(self, 'jobs'):
            for job in self['jobs']:
                self.jobs.append(Job(job))

class Job(dict):
    r"""Representation of a job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.job_id = get_value_or_default(self, 'job_id', None)
        self.api_version = get_value_or_default(self, 'api_version', None)
        self.path = get_value_or_default(self, 'path', None)
        self.status = get_value_or_default(self, 'status', None)
        self.progress = get_value_or_default(self, 'progress', 0)
        self.duration = get_value_or_default(self, 'duration', 0.0)
        self.time_submitted = get_value_or_default(self, 'time_submitted', None)
        self.time_started = get_value_or_default(self, 'time_started', None)
        self.time_completed = get_value_or_default(self, 'time_completed', None)
        self.expiry = get_value_or_default(self, 'expiry', None)
