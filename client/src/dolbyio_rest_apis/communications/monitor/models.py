"""
dolbyio_rest_apis.communications.monitor.models
~~~~~~~~~~~~~~~

This module contains the models used by the Dolby.io APIs.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default, in_and_not_none
from typing import List

class PagedResponse(dict):
    """Representation of a paged response."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.first = get_value_or_default(self, 'first', None)
        self.next = get_value_or_default(self, 'next', None)

class ConferenceOwner(dict):
    """Representation of a Conference Owner."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.user_id = get_value_or_default(self, 'userID', None)

        if in_and_not_none(self, 'metadata'):
            self.metadata = UserMetadata(self['metadata'])

class ConferenceStatisticsMaxParticipants(dict):
    """Representation of a Conference Statistics Max Participants."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.user = get_value_or_default(self, 'USER', 0)
        self.listener = get_value_or_default(self, 'LISTENER', 0)
        self.mixer = get_value_or_default(self, 'MIXER', 0)
        self.pstn = get_value_or_default(self, 'PSTN', 0)

class ConferenceParticipant(dict):
    """Representation of a Conference Participant."""

    def __init__(self, user_id, dictionary: dict):
        self.user_id = user_id
        dict.__init__(self, dictionary)

        #if in_and_not_none(self, 'connections'):
        #    self.connections = ConferenceOwner(self['connections'])

        #if in_and_not_none(self, 'stats'):
        #    self.stats = ConferenceStatistics(self['stats'])

class ConferenceParticipants(PagedResponse):
    """Representation of a Conference participants."""

    def __init__(self, dictionary: dict):
        PagedResponse.__init__(self, dictionary)

        self.participants: List[ConferenceParticipant] = []
        if in_and_not_none(self, 'participants'):
            for key in self['participants'].keys():
                participant = ConferenceParticipant(key, self['participants'][key])
                self.participants.append(participant)

class ConferenceStatisticsMaxRate(dict):
    """Representation of a Conference Statistics Max Rate."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.dtls = get_value_or_default(self, 'DTLS', 0)
        self.rtcp = get_value_or_default(self, 'RTCP', 0)
        self.rtp = get_value_or_default(self, 'RTP', 0)
        self.stun = get_value_or_default(self, 'STUN', 0)

class ConferenceStatisticsMaxStreams(dict):
    """Representation of a Conference Statistics Max Streams."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.audio = get_value_or_default(self, 'AUDIO', 0)
        self.video = get_value_or_default(self, 'VIDEO', 0)
        self.screenshare = get_value_or_default(self, 'SCREENSHARE', 0)

class ConferenceStatisticsNetwork(dict):
    """Representation of a Conference Statistics Network."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        if in_and_not_none(self, 'maxRxBytesRate'):
            self.max_rx_bytes_rate = ConferenceStatisticsMaxRate(self['maxRxBytesRate'])
        if in_and_not_none(self, 'maxRxPacketsRate'):
            self.max_rx_packets_rate = ConferenceStatisticsMaxRate(self['maxRxPacketsRate'])
        if in_and_not_none(self, 'maxRxStreams'):
            self.max_rx_streams = ConferenceStatisticsMaxStreams(self['maxRxStreams'])
        if in_and_not_none(self, 'maxTxBytesRate'):
            self.max_tx_bytes_rate = ConferenceStatisticsMaxRate(self['maxTxBytesRate'])
        if in_and_not_none(self, 'maxTxPacketsRate'):
            self.max_tx_packets_rate = ConferenceStatisticsMaxRate(self['maxTxPacketsRate'])
        if in_and_not_none(self, 'maxTxStreams'):
            self.max_tx_streams = ConferenceStatisticsMaxStreams(self['maxTxStreams'])

class ConferenceStatistics(dict):
    """Representation of a Conference Statistics."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        if in_and_not_none(self, 'maxParticipants'):
            self.max_participants = ConferenceStatisticsMaxParticipants(self['maxParticipants'])

        if in_and_not_none(self, 'network'):
            self.network = ConferenceStatisticsNetwork(self['network'])

class ConferenceSummary(dict):
    """Representation of a Conference Summary."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.conf_id = get_value_or_default(self, 'confId', None)
        self.alias = get_value_or_default(self, 'alias', None)
        self.region = get_value_or_default(self, 'region', None)
        self.start = get_value_or_default(self, 'start', 0)
        self.live = get_value_or_default(self, 'live', False)
        self.end = get_value_or_default(self, 'end', 0)
        self.duration = get_value_or_default(self, 'duration', 0)
        self.type = get_value_or_default(self, 'type', None)
        self.presence_duration = get_value_or_default(self, 'presenceDuration', 0)
        self.recording_duration = get_value_or_default(self, 'recordingDuration', 0)
        self.mixer_live_recording = get_value_or_default(self, 'mixerLiveRecording', 0)
        self.mixer_hls_streaming = get_value_or_default(self, 'mixerHlsStreaming', 0)
        self.mixer_rtmp_streaming = get_value_or_default(self, 'mixerRtmpStreaming', 0)
        self.nb_users = get_value_or_default(self, 'nbUsers', 0)
        self.nb_listeners = get_value_or_default(self, 'nbListeners', 0)
        self.nb_pstn = get_value_or_default(self, 'nbPstn', 0)

        if in_and_not_none(self, 'owner'):
            self.mix = ConferenceOwner(self['owner'])

        if in_and_not_none(self, 'statistics'):
            self.statistics = ConferenceStatistics(self['statistics'])

class GetConferencesResponse(PagedResponse):
    """Representation of a Conferences response."""

    def __init__(self, dictionary: dict):
        PagedResponse.__init__(self, dictionary)

        self.conferences: List[ConferenceSummary] = []
        if in_and_not_none(self, 'conferences'):
            for conference in self['conferences']:
                self.conferences.append(ConferenceSummary(conference))

class RecordingMix(dict):
    """Representation of a Recording Mix."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.mp4 = get_value_or_default(self, 'mp4', 0)
        self.mp3 = get_value_or_default(self, 'mp3', 0)
        self.region = get_value_or_default(self, 'region', None)

class UserMetadata(dict):
    """Representation of a User Metadata."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.user_id = get_value_or_default(self, 'userID', None)
        self.external_name = get_value_or_default(self, 'externalName', None)
        self.external_id = get_value_or_default(self, 'externalId', None)
        self.external_photo_url = get_value_or_default(self, 'externalPhotoUrl', None)
        self.ip_address = get_value_or_default(self, 'ipAddress', None)

class RecordingSplit(dict):
    """Representation of a Recording Split."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.start_time = get_value_or_default(self, 'startTime', 0)
        self.duration = get_value_or_default(self, 'duration', 0)
        self.size = get_value_or_default(self, 'size', 0)
        self.file_name = get_value_or_default(self, 'fileName', None)
        self.url = get_value_or_default(self, 'url', None)

        if in_and_not_none(self, 'metadata'):
            self.metadata = UserMetadata(self['metadata'])

class RecordingRecord(dict):
    """Representation of a Recording Record."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.start_time = get_value_or_default(self, 'startTime', 0)
        self.duration = get_value_or_default(self, 'duration', 0)
        self.size = get_value_or_default(self, 'size', 0)
        self.file_name = get_value_or_default(self, 'fileName', None)
        self.url = get_value_or_default(self, 'url', None)

        self.splits = []
        if in_and_not_none(self, 'splits'):
            for split in self['splits']:
                self.splits.append(RecordingSplit(split))

class RecordingAudio(dict):
    """Representation of a Recording Audio."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.region = get_value_or_default(self, 'region', None)

        if in_and_not_none(self, 'mix'):
            self.mix = RecordingMix(self['mix'])

        self.records = []
        if in_and_not_none(self, 'records'):
            for record in self['records']:
                self.records.append(RecordingRecord(record))

class Recording(dict):
    """Representation of a Recording."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.conf_id = get_value_or_default(self, 'confId', None)
        self.alias = get_value_or_default(self, 'alias', None)
        self.duration = get_value_or_default(self, 'duration', 0)
        self.ts = get_value_or_default(self, 'ts', 0)
        self.region = get_value_or_default(self, 'region', None)

        if in_and_not_none(self, 'mix'):
            self.mix = RecordingMix(self['mix'])

        if in_and_not_none(self, 'audio'):
            self.audio = RecordingAudio(self['audio'])

class GetRecordingsResponse(PagedResponse):
    """Representation of a Recordings response."""

    def __init__(self, dictionary: dict):
        PagedResponse.__init__(self, dictionary)

        self.recordings = []
        if in_and_not_none(self, 'recordings'):
            for recording in self['recordings']:
                self.recordings.append(Recording(recording))

class DolbyVoiceRecording(dict):
    """Representation of a Dolby Voice Recording."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.region = get_value_or_default(self, 'region', None)
        self.conf_id = None
        self.conf_alias = None
        if in_and_not_none(self, 'conference'):
            self.conf_id = get_value_or_default(self, 'confId', None)
            self.conf_alias = get_value_or_default(self, 'confAlias', None)

        self.records = []
        if in_and_not_none(self, 'records'):
            for record in self['records']:
                self.records.append(RecordingRecord(record))

class WebHookResponse(dict):
    """Representation of a WebHook event response."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.status = get_value_or_default(self, 'status', None)
        self.headers = get_value_or_default(self, 'headers', None)

class WebHook(dict):
    """Representation of a WebHook event."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.id = get_value_or_default(self, 'id', None)
        self.webhook = get_value_or_default(self, 'webhook', None)
        self.url = get_value_or_default(self, 'url', None)
        self.conf_id = get_value_or_default(self, 'confId', None)
        self.third_party_id = get_value_or_default(self, 'thirdPartyId', None)
        self.ts = get_value_or_default(self, 'ts', None)

        if in_and_not_none(self, 'response'):
            self.response = WebHookResponse(self['response'])

class GetWebHookResponse(PagedResponse):
    """Representation of a WebHook response."""

    def __init__(self, dictionary: dict):
        PagedResponse.__init__(self, dictionary)

        self.webhooks = []
        if in_and_not_none(self, 'webhooks'):
            for wbk in self['webhooks']:
                self.webhooks.append(WebHook(wbk))
