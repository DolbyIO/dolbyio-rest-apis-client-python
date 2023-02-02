"""
dolbyio_rest_apis.streaming.models.publish_token
~~~~~~~~~~~~~~~

This module contains the models used by the Publish Token models.
"""

from typing import List
from dolbyio_rest_apis.core.helpers import get_value_or_default

class PublishTokenStream(dict):
    """The :class:`PublishTokenStream` object, which represents a Publish Token Stream."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.stream_name = get_value_or_default(self, 'streamName', None)
        self.is_regex = get_value_or_default(self, 'isRegex', False)

class PublishToken(dict):
    """The :class:`PublishToken` object, which represents a Publish Token."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.id = get_value_or_default(self, 'id', None)
        self.label = get_value_or_default(self, 'label', None)
        self.token = get_value_or_default(self, 'token', None)
        self.added_on = get_value_or_default(self, 'addedOn', None)
        self.expires_on = get_value_or_default(self, 'expiresOn', None)
        self.is_active = get_value_or_default(self, 'isActive', None)
        self.streams = []
        for stream in self['streams']:
            self.streams.append(PublishTokenStream(stream))
        self.allowed_origins = get_value_or_default(self, 'allowedOrigins', None)
        self.allowed_ip_addresses = get_value_or_default(self, 'allowedIpAddresses', None)
        self.bind_ips_on_usage = get_value_or_default(self, 'bindIpsOnUsage', None)
        self.allowed_countries = get_value_or_default(self, 'allowedCountries', None)
        self.denied_countries = get_value_or_default(self, 'deniedCountries', None)
        self.origin_cluster = get_value_or_default(self, 'originCluster', None)
        self.subscribe_requires_auth = get_value_or_default(self, 'subscribeRequiresAuth', False)
        self.record = get_value_or_default(self, 'record', False)
        self.multisource = get_value_or_default(self, 'multisource', False)

class CreateUpdatePublishTokenStream():
    """The :class:`CreateUpdatePublishTokenStream` object, which represents a Publish Token Stream."""

    def __init__(self, stream_name: str, is_regex: bool):
        self.stream_name = stream_name
        self.is_regex = is_regex

class UpdatePublishToken():
    """The :class:`UpdatePublishToken` object, which represents an Update Publish Token request."""

    def __init__(self):
        self.label: str | None = None
        self.refresh_token: bool | None = None
        self.is_active: bool | None = None
        self.add_token_streams: List[CreateUpdatePublishTokenStream] | None = None
        self.remove_token_streams: List[CreateUpdatePublishTokenStream] | None = None
        self.update_allowed_origins: List[str] | None = None
        self.update_allowed_ip_addresses: List[str] | None = None
        self.update_bind_ips_on_usage: int | None = None
        self.update_allowed_countries: List[str] | None = None
        self.update_denied_countries: List[str] | None = None
        self.update_origin_cluster: str | None = None
        self.subscribe_requires_auth: bool | None = None
        self.record: bool | None = None
        self.multisource: bool | None = None

class CreatePublishToken():
    """The :class:`CreatePublishToken` object, which represents a Create Publish Token request."""

    def __init__(self, label: str):
        self.label = label
        self.expires_on: str | None = None
        self.streams: List[CreateUpdatePublishTokenStream] = []
        self.allowed_origins: List[str] | None = None
        self.allowed_ip_addresses: List[str] | None = None
        self.bind_ips_on_usage: int | None = None
        self.allowed_countries: List[str] | None = None
        self.denied_countries: List[str] | None = None
        self.origin_cluster: str | None = None
        self.subscribe_requires_auth: bool = False
        self.record: bool = False
        self.multisource: bool = False

class ActivePublishToken(dict):
    """The :class:`ActivePublishToken` object."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.token_ids: List[int] = []
        for tid in self['tokenIds']:
            self.token_ids.append(tid)

class FailedToken(dict):
    """The :class:`FailedToken` object, which represents a Failed Token."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.token_id = get_value_or_default(self, 'tokenId', None)
        self.error_message = get_value_or_default(self, 'errorMessage', None)

class DisablePublishTokenResponse(dict):
    """The :class:`DisablePublishTokenResponse` object, which represents a the response to the disable publish token."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.successful_tokens = get_value_or_default(self, 'successfulTokens', None)
        self.failed_tokens: List[int] = []
        for ft in self['failedTokens']:
            self.failed_tokens.append(FailedToken(ft))
