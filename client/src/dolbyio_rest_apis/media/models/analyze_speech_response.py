"""
dolbyio_rest_apis.media.models.analyze_speech_response
~~~~~~~~~~~~~~~

This module contains the Analyze Speech model.
"""

from .job_response import JobResponse

class AnalyzeSpeechJobResult(dict):
    """The :class:`AnalyzeSpeechJobResult` object, which represents the result for an analyze speech job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

class AnalyzeSpeechJob(JobResponse):
    """The :class:`AnalyzeSpeechJob` object, which represents the result for an analyze speech job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = AnalyzeSpeechJobResult(dictionary['result'])
