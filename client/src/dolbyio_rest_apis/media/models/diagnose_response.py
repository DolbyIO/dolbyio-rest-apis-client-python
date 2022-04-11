"""
dolbyio_rest_apis.media.models.diagnose_response
~~~~~~~~~~~~~~~

This module contains the Diagnose Response model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default
from .job_response import JobResponse

class DiagnoseJobResult(dict):
    """The :class:`DiagnoseJobResult` object, which represents the result for a diagnose job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.version = get_value_or_default(dictionary, 'version', None)

class DiagnoseJob(JobResponse):
    """The :class:`DiagnoseJob` object, which represents the result for a diagnose job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = DiagnoseJobResult(dictionary)
