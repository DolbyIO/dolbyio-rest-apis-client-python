"""
dolbyio_rest_apis.media.models.job_response
~~~~~~~~~~~~~~~

This module contains the Job response base model
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default
from .result_error import ResultError

class JobResponse(dict):
    """The :class:`JobResult` object, which represents the result for a job operation."""

    def __init__(self, job_id, dictionary: dict):
        dict.__init__(self, dictionary)

        self.job_id = job_id
        self.api_version = get_value_or_default(dictionary, 'api_version', None)
        self.path = get_value_or_default(dictionary, 'path', None)
        self.status = get_value_or_default(dictionary, 'status', None)
        self.progress = get_value_or_default(dictionary, 'progress', 0)
        self.result = None

        if 'error' in dictionary:
            self.error = ResultError(dictionary['error'])

