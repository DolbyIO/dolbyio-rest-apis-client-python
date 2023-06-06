"""
dolbyio_rest_apis.media.models.analyze_music_response
~~~~~~~~~~~~~~~

This module contains the Analyze Music model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default, in_and_not_none
from .job_response import JobResponse

class AnalyzeMusicJobResultMediaInfoContainer(dict):
    """The :class:`AnalyzeMusicJobResultMediaInfoContainer` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.kind = get_value_or_default(dictionary, 'kind', None)
        self.duration = get_value_or_default(dictionary, 'duration', None)
        self.bitrate = get_value_or_default(dictionary, 'bitrate', None)
        self.size = get_value_or_default(dictionary, 'size', None)

class AnalyzeMusicJobResultMediaInfoAudio(dict):
    """The :class:`AnalyzeMusicJobResultMediaInfoAudio` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.codec = get_value_or_default(dictionary, 'codec', None)
        self.bit_depth = get_value_or_default(dictionary, 'bit_depth', None)
        self.channels = get_value_or_default(dictionary, 'channels', None)
        self.sample_rate = get_value_or_default(dictionary, 'sample_rate', None)
        self.duration = get_value_or_default(dictionary, 'duration', None)
        self.bitrate = get_value_or_default(dictionary, 'bitrate', None)

class AnalyzeMusicJobResultMediaInfoVideo(dict):
    """The :class:`AnalyzeMusicJobResultMediaInfoVideo` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.codec = get_value_or_default(dictionary, 'codec', None)
        self.frame_rate = get_value_or_default(dictionary, 'frame_rate', None)
        self.height = get_value_or_default(dictionary, 'height', None)
        self.width = get_value_or_default(dictionary, 'width', None)
        self.duration = get_value_or_default(dictionary, 'duration', None)
        self.bitrate = get_value_or_default(dictionary, 'bitrate', None)

class AnalyzeMusicJobResultMediaInfo(dict):
    """The :class:`AnalyzeMusicJobResultMediaInfo` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        if 'container' in dictionary:
            self.container = AnalyzeMusicJobResultMediaInfoContainer(dictionary['container'])
        if 'audio' in dictionary:
            self.audio = AnalyzeMusicJobResultMediaInfoAudio(dictionary['audio'])
        if 'container' in dictionary:
            self.container = AnalyzeMusicJobResultMediaInfoVideo(dictionary['container'])

class AnalyzeMusicJobResultProcessedRegionAudioMusicSection(dict):
    """The :class:`AnalyzeMusicJobResultProcessedRegionAudioMusicSection` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.loudness = get_value_or_default(dictionary, 'loudness', None)
        self.bpm = get_value_or_default(dictionary, 'bpm', None)
        self.key = []
        if in_and_not_none(self, 'key'):
            for k in self['key']:
                self.key.append(k)
        self.genre = []
        if in_and_not_none(self, 'genre'):
            for g in self['genre']:
                self.genre.append(g)
        self.era = []
        if in_and_not_none(self, 'era'):
            for e in self['era']:
                self.era.append(e)
        self.instrument = []
        if in_and_not_none(self, 'instrument'):
            for i in self['instrument']:
                self.era.append(i)

class AnalyzeMusicJobResultProcessedRegionAudioMusic(dict):
    """The :class:`AnalyzeMusicJobResultProcessedRegionAudioMusic` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.percentage = get_value_or_default(dictionary, 'percentage', None)
        self.num_sections = get_value_or_default(dictionary, 'num_sections', None)
        self.sections = []
        if in_and_not_none(self, 'sections'):
            for s in self['sections']:
                self.sections.append(AnalyzeMusicJobResultProcessedRegionAudioMusicSection(s))

class AnalyzeMusicJobResultProcessedRegionAudio(dict):
    """The :class:`AnalyzeMusicJobResultProcessedRegionAudio` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        if 'music' in dictionary:
            self.music = AnalyzeMusicJobResultProcessedRegionAudioMusic(dictionary['music'])

class AnalyzeMusicJobResultProcessedRegion(dict):
    """The :class:`AnalyzeMusicJobResultProcessedRegion` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.start = get_value_or_default(dictionary, 'start', None)
        self.end = get_value_or_default(dictionary, 'end', None)

class AnalyzeMusicJobResult(dict):
    """The :class:`AnalyzeMusicJobResult` object, which represents the result for an analyze music job."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        if 'media_info' in dictionary:
            self.media_info = AnalyzeMusicJobResultMediaInfo(dictionary['media_info'])
        if 'processed_region' in dictionary:
            self.media_info = AnalyzeMusicJobResultProcessedRegion(dictionary['processed_region'])

class AnalyzeMusicJob(JobResponse):
    """The :class:`AnalyzeMusicJob` object, which represents the result for an analyze music job."""

    def __init__(self, job_id, dictionary: dict):
        JobResponse.__init__(self, job_id, dictionary)

        if 'result' in dictionary:
            self.result = AnalyzeMusicJobResult(dictionary['result'])
