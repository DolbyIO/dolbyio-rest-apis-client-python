"""
dolbyio_rest_apis.communications.models
~~~~~~~~~~~~~~~

This module contains the models used by the Dolby.io APIs.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default, in_and_not_none
from enum import Enum
from dataclasses import dataclass
from typing import List

class AccessToken(dict):
    """The :class:`AccessToken` object, which represents the access token."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.token_type = get_value_or_default(self, 'token_type', None)
        self.access_token = get_value_or_default(self, 'access_token', None)
        self.refresh_token = get_value_or_default(self, 'refresh_token', None)
        self.expires_in_val = get_value_or_default(self, 'expires_in', 0)

class Participant:
    """The :class:`Participant` object, which represents a participant's permissions."""

    def __init__(self, external_id, permissions, notify):
        self.external_id = external_id
        self.permissions = permissions
        self.notify = notify

class RTCPMode(str, Enum):
    """The :class:`RTCPMode` enumeration, which represents the possible RTCP modes."""

    WORST = 'worst'
    '''Adjusts the transmission bitrate to the receiver who has the worst network conditions.'''

    AVERAGE = 'average'
    '''Averages the available bandwidth of all the receivers and adjusts the transmission bitrate to this value.'''

    MAX = 'max'
    '''Does not adjust the transmission bitrate to the receiver’s bandwidth.'''

class VideoCodec(str, Enum):
    """The :class:`VideoCodec` enumeration, which represents the possible video codecs."""

    VP8 = 'VP8'
    H264 = 'H264'

class Permission(str, Enum):
    """The :class:`Permission` enumeration, which represents the possible participant's permissions."""

    INVITE = 'INVITE'
    '''Allows a participant to invite participants to a conference.'''

    JOIN = 'JOIN'
    '''Allows a participant to join a conference.'''

    SEND_AUDIO = 'SEND_AUDIO'
    '''Allows a participant to send an audio stream during a conference.'''

    SEND_VIDEO = 'SEND_VIDEO'
    '''Allows a participant to send a video stream during a conference.'''

    SHARE_SCREEN = 'SHARE_SCREEN'
    '''Allows a participant to share their screen during a conference.'''

    SHARE_VIDEO = 'SHARE_VIDEO'
    '''Allows a participant to share a video during a conference.'''

    SHARE_FILE = 'SHARE_FILE'
    '''Allows a participant to share a file during a conference.'''

    SEND_MESSAGE = 'SEND_MESSAGE'
    '''Allows a participant to send a message to other participants during a conference.'''

    RECORD = 'RECORD'
    '''Allows a participant to record a conference.'''

    STREAM = 'STREAM'
    '''Allows a participant to stream a conference.'''

    KICK = 'KICK'
    '''Allows a participant to kick other participants from a conference.'''

    UPDATE_PERMISSIONS = 'UPDATE_PERMISSIONS'
    '''Allows a participant to update other participants' permissions.'''

@dataclass
class UserToken:
    """Representation of a User access token."""
    external_id: str
    token: str

class Conference(dict):
    """Representation of a newly created Conference."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.conference_id = get_value_or_default(self, 'conferenceId', None)
        self.conference_alias = get_value_or_default(self, 'conferenceAlias', None)
        self.conference_pincode = get_value_or_default(self, 'conferencePincode', None)
        self.is_protected = get_value_or_default(self, 'isProtected', False)
        self.owner_token = get_value_or_default(self, 'ownerToken', None)

        self.user_tokens: List[UserToken] = []
        if in_and_not_none(self, 'usersTokens'):
            for key in self['usersTokens'].keys():
                user_token = UserToken(key, self['usersTokens'][key])
                self.user_tokens.append(user_token)

class RemixStatus(dict):
    """Representation of a Remix Status."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.status = get_value_or_default(self, 'status', None)
        self.region = get_value_or_default(self, 'region', None)
        self.alias = get_value_or_default(self, 'alias', None)

@dataclass
class Coordinates:
    """Representation of a Coordinate object."""
    x: int
    y: int
    z: int

@dataclass
class SpatialAudioEnvironment:
    """
    The spatial environment of an application,
    so the audio renderer understands which directions the application considers
    forward, up, and right and which units it uses for distance.
    """
    scale: Coordinates
    forward: Coordinates
    up: Coordinates
    right: Coordinates

@dataclass
class SpatialAudioListener:
    """Representation of the listener's audio position and direction, defined using Cartesian coordinates."""
    position: Coordinates
    direction: Coordinates

@dataclass
class SpatialAudioUser:
    """Representation of the user's position, defined using Cartesian coordinates."""
    external_id: str
    position: Coordinates
