"""
dolbyio_rest_apis.streaming.models.publish_token
~~~~~~~~~~~~~~~

This module contains the models used by the Publish Token module.
"""

from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TokenGeoCascade:
    """The :class:`TokenGeoCascade` object, the definition of the geo cascading rules for a publish token."""

    is_enabled: bool = False
    clusters: list[str] = field(default_factory=lambda: [])

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TokenStreamName:
    """The :class:`TokenStreamName` object, which represents a token stream name."""

    stream_name: str
    is_regex: bool = False

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PublishTokenRestream:
    """The :class:`PublishTokenRestream` object, the definition of a restream endpoint."""

    url: str
    key: str

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TokenEffectiveSettings:
    """The :class:`TokenEffectiveSettings` object, which represents the effective settings for a publish token."""

    origin_cluster: str | None = None
    allowed_countries: list[str] = field(default_factory=lambda: [])
    denied_countries: list[str] = field(default_factory=lambda: [])
    geo_cascade: TokenGeoCascade | None = None

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PublishToken:
    """The :class:`PublishToken` object, which represents a publish token."""

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
    subscribe_requires_auth: bool = False
    record: bool = False
    clip: bool = False
    multisource: bool = False
    low_latency_rtmp: bool = False
    enable_thumbnails: bool = False
    display_srt_passphrase: bool = False
    srt_passphrase: bool = False
    geo_cascade: TokenGeoCascade | None = None
    restream: list[PublishTokenRestream] = field(default_factory=lambda: [])
    effective_settings: TokenEffectiveSettings | None = None

class UpdatePublishToken:
    """The :class:`UpdatePublishToken` object, which represents an Update Publish Token request."""

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
        self.subscribe_requires_auth: bool | None = None
        self.record: bool | None = None
        self.multisource: bool | None = None
        self.enable_thumbnails: bool | None = None
        self.display_srt_passphrase: bool | None = None
        self.low_latency_rtmp: bool | None = None
        self.clip: bool = False
        self.update_geo_cascade: TokenGeoCascade | None = None
        self.update_restream: list[PublishTokenRestream] | None = None

class CreatePublishToken:
    """The :class:`CreatePublishToken` object, which represents a Create Publish Token request."""

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
        self.subscribe_requires_auth: bool = False
        self.record: bool = False
        self.multisource: bool = False
        self.enable_thumbnails: bool = False
        self.display_srt_passphrase: bool = False
        self.low_latency_rtmp: bool = True
        self.geo_cascade: TokenGeoCascade | None = None
        self.clip: bool = False
        self.restream: list[PublishTokenRestream] = []

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ActivePublishToken:
    """The :class:`ActivePublishToken` object."""

    token_ids: list[int]

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FailedToken:
    """The :class:`FailedToken` object, which represents a Failed Token."""

    token_id: str | None = None
    error_message: str | None = None

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DisablePublishTokenResponse:
    """The :class:`DisablePublishTokenResponse` object, which represents a the response to the disable publish token."""

    successful_tokens: list[int]
    failed_tokens: list[FailedToken]
