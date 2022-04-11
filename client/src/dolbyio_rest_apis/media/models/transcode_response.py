"""
dolbyio_rest_apis.media.models.transcode_response
~~~~~~~~~~~~~~~

This module contains the Transcode Response model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default
from .job_response import JobResponse

class TranscodeJobResult(dict):
    """The :class:`TranscodeJobResult` object, which represents the result for a transcode job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.version = get_value_or_default(dictionary, 'version', None)

class TranscodeJob(JobResponse):
    """The :class:`TranscodeJob` object, which represents the result for a transcode job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = TranscodeJobResult(dictionary)
