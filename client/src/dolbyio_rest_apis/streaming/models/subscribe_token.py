"""
dolbyio_rest_apis.streaming.models.subscribe_token
~~~~~~~~~~~~~~~

This module contains the models used by the Subscribe Token module.
"""

from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json
from dolbyio_rest_apis.streaming.models.publish_token import TokenEffectiveSettings, TokenStreamName

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SubscribeToken:
    """The :class:`SubscribeToken` object, which represents a Subscribe Token."""

    id: int | None = None
    label: str | None = None
    token: str | None = None
    added_on: str | None = None
    expires_on: str | None = None
    is_active: bool | None = None
    streams: list[TokenStreamName] = field(default_factory=lambda: [])
    allowed_origins: list[str] = field(default_factory=lambda: [])
    allowed_ip_addresses: list[str] = field(default_factory=lambda: [])
    bind_ips_on_usage: int | None = None
    allowed_countries: list[str] = field(default_factory=lambda: [])
    denied_countries: list[str] = field(default_factory=lambda: [])
    origin_cluster: str | None = None
    effective_settings: TokenEffectiveSettings | None = None

class UpdateSubscribeToken:
    """The :class:`UpdateSubscribeToken` object, which represents an Update Subscribe Token request."""

    def __init__(self):
        self.label: str | None = None
        self.refresh_token: bool | None = None
        self.is_active: bool | None = None
        self.add_token_streams: list[TokenStreamName] | None = None
        self.remove_token_streams: list[TokenStreamName] | None = None
        self.update_allowed_origins: list[str] | None = None
        self.update_allowed_ip_addresses: list[str] | None = None
        self.update_bind_ips_on_usage: int | None = None
        self.update_allowed_countries: list[str] | None = None
        self.update_denied_countries: list[str] | None = None
        self.update_origin_cluster: str | None = None

class CreateSubscribeToken():
    """The :class:`CreateSubscribeToken` object, which represents a Create Subscribe Token request."""

    def __init__(self, label: str):
        self.label = label
        self.expires_on: str | None = None
        self.streams: list[TokenStreamName] = []
        self.allowed_origins: list[str] | None = None
        self.allowed_ip_addresses: list[str] | None = None
        self.bind_ips_on_usage: int | None = None
        self.allowed_countries: list[str] | None = None
        self.denied_countries: list[str] | None = None
        self.origin_cluster: str | None = None
        self.tracking_id: str | None = None
