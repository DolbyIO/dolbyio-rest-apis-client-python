"""
dolbyio_rest_apis.media.models.mastering_response
~~~~~~~~~~~~~~~

This module contains the Mastering Response model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default
from .job_response import JobResponse

class MasteringPreviewJobResult(dict):
    """The :class:`MasteringPreviewJobResult` object, which represents the result for a mastering preview job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.initial_level = get_value_or_default(dictionary, 'initial_level', None)

class MasteringPreviewJob(JobResponse):
    """The :class:`MasteringPreviewJob` object, which represents the result for a mastering preview job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = MasteringPreviewJobResult(dictionary)

class MasteringJobResult(MasteringPreviewJobResult):
    """The :class:`MasteringJobResult` object, which represents the result for a mastering job."""

    def __init__(self, dictionary: dict):
        MasteringPreviewJobResult.__init__(self, dictionary)

        self.final_level = get_value_or_default(dictionary, 'final_level', None)

class MasteringJob(JobResponse):
    """The :class:`MasteringJob` object, which represents the result for a mastering job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = MasteringJobResult(dictionary)
