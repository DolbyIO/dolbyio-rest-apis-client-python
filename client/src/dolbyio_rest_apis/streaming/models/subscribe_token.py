"""
dolbyio_rest_apis.streaming.models.subscribe_token
~~~~~~~~~~~~~~~

This module contains the models used by the Subscribe Token models.
"""

from typing import List
from dolbyio_rest_apis.core.helpers import get_value_or_default

class SubscribeTokenStream(dict):
    """The :class:`SubscribeTokenStream` object, which represents a Subscribe Token Stream."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.stream_name = get_value_or_default(self, 'streamName', None)
        self.is_regex = get_value_or_default(self, 'isRegex', False)

class SubscribeToken(dict):
    """The :class:`SubscribeToken` object, which represents a Subscribe Token."""

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
            self.streams.append(SubscribeTokenStream(stream))
        self.allowed_origins = get_value_or_default(self, 'allowedOrigins', None)
        self.allowed_ip_addresses = get_value_or_default(self, 'allowedIpAddresses', None)
        self.bind_ips_on_usage = get_value_or_default(self, 'bindIpsOnUsage', None)
        self.allowed_countries = get_value_or_default(self, 'allowedCountries', None)
        self.denied_countries = get_value_or_default(self, 'deniedCountries', None)
        self.origin_cluster = get_value_or_default(self, 'originCluster', None)

class CreateUpdateSubscribeTokenStream():
    """The :class:`UpdateSubscribeTokenStream` object, which represents an update Subscribe Token Stream."""

    def __init__(self, stream_name: str, is_regex: bool):
        self.stream_name = stream_name
        self.is_regex = is_regex

class UpdateSubscribeToken():
    """The :class:`UpdateSubscribeToken` object, which represents an Update Subscribe Token request."""

    def __init__(self):
        self.label: str | None = None
        self.refresh_token: bool | None = None
        self.is_active: bool | None = None
        self.add_token_streams: List[CreateUpdateSubscribeTokenStream] | None = None
        self.remove_token_streams: List[CreateUpdateSubscribeTokenStream] | None = None
        self.update_allowed_origins: List[str] | None = None
        self.update_allowed_ip_addresses: List[str] | None = None
        self.update_bind_ips_on_usage: int | None = None
        self.update_allowed_countries: List[str] | None = None
        self.update_denied_countries: List[str] | None = None
        self.update_origin_cluster: str | None = None

class CreateSubscribeToken():
    """The :class:`CreateSubscribeToken` object, which represents a Create Subscribe Token request."""

    def __init__(self, label: str):
        self.label = label
        self.expires_on: str | None = None
        self.streams: List[CreateUpdateSubscribeTokenStream] = []
        self.allowed_origins: List[str] | None = None
        self.allowed_ip_addresses: List[str] | None = None
        self.bind_ips_on_usage: int | None = None
        self.allowed_countries: List[str] | None = None
        self.denied_countries: List[str] | None = None
        self.origin_cluster: str | None = None
