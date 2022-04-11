"""
dolbyio_rest_apis.media.models.enhance_response
~~~~~~~~~~~~~~~

This module contains the Enhance Response model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default
from .job_response import JobResponse

class EnhanceJobResult(dict):
    """The :class:`EnhanceJobResult` object, which represents the result for an enhance job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.version = get_value_or_default(dictionary, 'version', None)

class EnhanceJob(JobResponse):
    """The :class:`EnhanceJob` object, which represents the result for an enhance job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = EnhanceJobResult(dictionary)
