"""
dolbyio_rest_apis.media.models.analyze_response
~~~~~~~~~~~~~~~

This module contains the Analyze models.
"""

from .job_response import JobResponse

class AnalyzeJobResult(dict):
    """The :class:`AnalyzeJobResult` object, which represents the result for an analyze job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        if 'media_info' in dictionary:
            self.media_info = dictionary['media_info']
        if 'processed_region' in dictionary:
            self.media_info = dictionary['processed_region']

class AnalyzeJobResponse(JobResponse):
    """The :class:`AnalyzeJobResponse` object, which represents the result for an analyze job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = AnalyzeJobResult(dictionary)
