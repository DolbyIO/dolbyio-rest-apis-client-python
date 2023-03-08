"""
dolbyio_rest_apis.media.models.analyze_music_response
~~~~~~~~~~~~~~~

This module contains the Analyze Music model.
"""

from .job_response import JobResponse

class AnalyzeMusicJobResult(dict):
    """The :class:`AnalyzeMusicJobResult` object, which represents the result for an analyze music job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        if 'media_info' in dictionary:
            self.media_info = dictionary['media_info']
        if 'processed_region' in dictionary:
            self.media_info = dictionary['processed_region']

class AnalyzeMusicJob(JobResponse):
    """The :class:`AnalyzeMusicJob` object, which represents the result for an analyze music job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = AnalyzeMusicJobResult(dictionary)
