"""
dolbyio_rest_apis.communications.conference
~~~~~~~~~~~~~~~

This module contains the functions to work with the conference API.
"""

from dataclasses import asdict
from dolbyio_rest_apis.core.helpers import get_value, add_if_not_none
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_comms_url_v2
from .models import UserToken, Conference, SpatialAudioEnvironment, SpatialAudioListener, SpatialAudioUser, RTCPMode, Participant, VideoCodec
from typing import List

async def create_conference(
        access_token: str,
        owner_external_id: str,
        alias: str=None,
        pincode: str=None,
        dolby_voice: bool=True,
        live_recording: bool=False,
        rtcp_mode: RTCPMode=RTCPMode.AVERAGE,
        ttl: int=None,
        video_codec: VideoCodec=None,
        audio_only: bool=False,
        participants: List[Participant]=None,
        recording_formats: List[str]=None,
        region: str=None,
    ) -> Conference:
    r"""
    Creates a conference.

    See: https://docs.dolby.io/communications-apis/reference/create-conference

    Args:
        access_token: Access token to use for authentication.
        owner_external_id: External ID of the conference owner.
        alias: (Optional) Name of the conference.
        pincode: (Optional)
        dolby_voice: (Optional) Indicates if Dolby Voice is enabled for the conference.
            The `True` value creates the conference with Dolby Voice enabled.
        live_recording: (Optional) Indicates if live recording is enabled for the conference.
        rtcp_mode: (Optional) Specifies the bitrate adaptation mode for the video transmission.
        ttl: (Optional) Specifies the time to live that enables customizing the waiting time
            (in seconds) and terminating empty conferences.
        audio_only: (Optional) If `True`, the conference does not allow participants to enable video.
        video_codec: (Optional) Specifies the video codec (VP8 or H264) for the conference.
        participants: List of the :class:`Participant` object to update the permissions.
        recording_formats: If specified, the default RecordingConfiguration is overridden.
            Specifies the recording format. Valid values are 'mp3' and 'mp4'.
        region: Dolby.io region where you want the conference to be hosted. Can be one of:
            - au: Australia
            - ca: Canada
            - eu: Europe
            - in: India
            - us: United States

    Returns:
        A :class:`Conference` object.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    parameters = {
        'dolbyVoice': dolby_voice,
        'liveRecording': live_recording,
        'rtcpMode': rtcp_mode.value,
    }
    add_if_not_none(parameters, 'pincode', pincode)
    add_if_not_none(parameters, 'ttl', ttl)
    add_if_not_none(parameters, 'audioOnly', audio_only)
    add_if_not_none(parameters, 'videoCodec', video_codec)

    if recording_formats is not None and len(recording_formats) > 0:
        parameters['recording'] = {
            'format': recording_formats
        }

    payload = {
        'ownerExternalId': owner_external_id,
        'parameters': parameters,
    }
    add_if_not_none(payload, 'alias', alias)

    if participants is not None and len(participants) > 0:
        obj_participants = { }

        for participant in participants:
            if isinstance(participant, Participant):
                permissions = []
                for p in participant.permissions:
                    permissions.append(get_value(p))

                obj_participants[participant.external_id] = {
                    'permissions': permissions,
                    'notification': participant.notify,
                }

        payload['participants'] = obj_participants

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2(region)}/conferences/create',
            payload=payload
        )

    return Conference(json_response)

async def invite(
        access_token: str,
        conference_id: str,
        participants: List[Participant],
    ) -> List[UserToken]:
    r"""
    Invites participants to an ongoing conference. This API can also be used to generate new conference access tokens
    for an ongoing conference. If the invite request includes participants that are already in the conference, a new
    conference access token is not generated and an invitation is not sent.

    See: https://docs.dolby.io/communications-apis/reference/invite-to-conference

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        participants: List of the :class:`Participant` object to invite to the conference.

    Returns:
        A list of :class:`UserToken` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    obj_participants = { }
    for participant in participants:
        if isinstance(participant, Participant):
            permissions = []
            for p in participant.permissions:
                permissions.append(get_value(p))

            obj_participants[participant.external_id] = {
                'permissions': permissions,
                'notification': participant.notify,
            }

    payload = {
        'participants': obj_participants,
    }

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/{conference_id}/invite',
            payload=payload
        )

    user_tokens = []
    for key in json_response.keys():
        user_token = UserToken(key, json_response[key])
        user_tokens.append(user_token)

    return user_tokens

async def kick(
        access_token: str,
        conference_id: str,
        external_ids: List[str],
    ) -> None:
    r"""
    Kicks participants from an ongoing conference.

    See: https://docs.dolby.io/communications-apis/reference/kick-from-conference

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        external_ids: List external IDs of the participants to kick out of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    payload = {
        'externalIds': external_ids,
    }

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/{conference_id}/kick',
            payload=payload
        )

async def send_message(
        access_token: str,
        conference_id: str,
        from_external_id: str,
        to_external_ids: List[str],
        message: str
    ) -> None:
    r"""
    Sends a message to some or all participants in a conference.

    See: https://docs.dolby.io/communications-apis/reference/send-message

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        from_external_id: The external ID of the author of the message.
        to_external_ids: A list of external IDs that will receive the message.
            If empty, the message will be broadcasted to all participants in the conference.
        message: The message to send.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    payload = {
        'from': from_external_id,
        'message': message,
    }

    if to_external_ids is not None and len(to_external_ids) > 0:
        payload['to'] = to_external_ids

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/{conference_id}/message',
            payload=payload
        )

async def set_spatial_listeners_audio(
        access_token: str,
        conference_id: str,
        environment: SpatialAudioEnvironment,
        listener: SpatialAudioListener,
        users: List[SpatialAudioUser],
    ) -> None:
    r"""
    Sets the spatial audio scene for all listeners in an ongoing conference.
    This sets the spatial audio environment, the position and direction for all listeners with the spatialAudio flag enabled.
    The calls are not cumulative, and each call sets all the spatial listener values.
    Participants who do not have a position set are muted.

    See: https://docs.dolby.io/communications-apis/reference/set-spatial-listeners-audio

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        environment: The spatial environment of an application,
            so the audio renderer understands which directions the application considers
            forward, up, and right and which units it uses for distance.
        listener: The listener's audio position and direction, defined using Cartesian coordinates.
        users: The users' audio positions, defined using Cartesian coordinates.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    obj_users = { }
    for user in users:
        obj_users[user.external_id] = asdict(user.position)

    payload = {
        'environment': asdict(environment),
        'listener': asdict(listener),
        'users': obj_users,
    }

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_put(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/{conference_id}/spatial-listeners-audio',
            payload=payload
        )

async def update_permissions(
        access_token: str,
        conference_id: str,
        participants: List[Participant],
    ) -> List[UserToken]:
    r"""
    Update permissions for participants in a conference. When a participant's permissions are updated, the new token
    is sent directly to the SDK. The SDK automatically receives, stores, and manages the new token
    and a permissionsUpdated event is sent.

    See: https://docs.dolby.io/communications-apis/reference/update-permissions

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.
        participants: List of the :class:`Participant` object to update the permissions.

    Returns:
        A list of :class:`UserToken` objects.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    obj_participants = { }
    for participant in participants:
        if isinstance(participant, Participant):
            permissions = []
            for p in participant.permissions:
                permissions.append(get_value(p))

            obj_participants[participant.external_id] = {
                'permissions': permissions,
            }

    payload = {
        'participants': obj_participants,
    }

    async with CommunicationsHttpContext() as http_context:
        json_response = await http_context.requests_post(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/{conference_id}/permissions',
            payload=payload
        )

    user_tokens = []
    for key in json_response.keys():
        user_token = UserToken(key, json_response[key])
        user_tokens.append(user_token)

    return user_tokens

async def terminate(
        access_token: str,
        conference_id: str,
    ) -> None:
    r"""
    Terminates an ongoing conference and removes all remaining participants from the conference.

    See: https://docs.dolby.io/communications-apis/reference/terminate-conference

    Args:
        access_token: Access token to use for authentication.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_delete(
            access_token=access_token,
            url=f'{get_comms_url_v2()}/conferences/{conference_id}',
        )
