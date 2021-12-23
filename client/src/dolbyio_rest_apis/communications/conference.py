"""
dolbyio_rest_apis.communications.conference
~~~~~~~~~~~~~~~

This module contains the functions to work with the conference API.
"""

from deprecated import deprecated
from dolbyio_rest_apis.core.helpers import get_value, add_if_not_none
from dolbyio_rest_apis.communications.internal.http_context import CommunicationsHttpContext
from dolbyio_rest_apis.communications.internal.urls import get_api_v2_url, get_session_url
from .models import UserToken, Conference, RTCPMode, Participant, VideoCodec
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
        participants: List[Participant]=None,
    ) -> Conference:
    r"""
    Creates a conference.

    See: https://docs.dolby.io/interactivity/reference/postconferencecreate

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
        video_codec: (Optional) Specifies video codecs (VP8 or H264) for a specific conference.
        participants: List of the :class:`Participant` object to update the permissions.

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
    add_if_not_none(parameters, 'videoCodec', video_codec)

    payload = {
        'ownerExternalId': owner_external_id,
        'parameters': parameters,
    }
    add_if_not_none(payload, 'alias', alias)

    if not participants is None and len(participants) > 0:
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
            url=f'{get_api_v2_url()}/conferences/create',
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

    See: https://docs.dolby.io/interactivity/reference/postconferenceinvite

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
            url=f'{get_api_v2_url()}/conferences/{conference_id}/invite',
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

    See: https://docs.dolby.io/interactivity/reference/postconferencekick

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
            url=f'{get_api_v2_url()}/conferences/{conference_id}/kick',
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

    See: https://docs.dolby.io/interactivity/reference/postconferencepermissions

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
            url=f'{get_api_v2_url()}/conferences/{conference_id}/permissions',
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

    See: https://docs.dolby.io/interactivity/reference/deleteconference

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
            url=f'{get_api_v2_url()}/conferences/{conference_id}',
        )

@deprecated(reason='This API is no longer applicable for applications on the new Dolby.io Communications APIs platform.')
async def destroy(
        consumer_key: str,
        consumer_secret: str,
        conference_id: str,
    ) -> None:
    r"""
    Destroys an ongoing conference and removes all remaining participants from the conference.

    See: https://docs.dolby.io/interactivity/reference/postconferencedestroy

    Args:
        consumer_key: Your Dolby.io Consumer Key.
        consumer_secret: Your Dolby.io Consumer Secret.
        conference_id: Identifier of the conference.

    Raises:
        HttpRequestError: If a client error one occurred.
        HTTPError: If one occurred.
    """

    async with CommunicationsHttpContext() as http_context:
        await http_context.requests_post_basic_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            url=f'{get_session_url()}/conferences/{conference_id}/destroy',
        )
