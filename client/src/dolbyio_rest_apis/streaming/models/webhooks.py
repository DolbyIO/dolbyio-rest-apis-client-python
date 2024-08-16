"""
dolbyio_rest_apis.streaming.models.webhooks
~~~~~~~~~~~~~~~

This module contains the models used by the Webhooks module.
"""

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Webhook:
    """The :class:`Webhook` object, which represents a webhook."""

    id: int | None = None
    url: str | None = None
    secret: str | None = None
    is_feed_hooks: bool | None = None
    is_recording_hooks: bool | None = None
    is_thumbnail_hooks: bool | None = None
    is_transcoder_hooks: bool | None = None
    is_clip_hooks: bool | None = None

class UpdateWebhook:
    """The :class:`UpdateWebhook` object, which represents an Update webhook request."""

    def __init__(self):
        self.url: str | None = None
        self.refresh_secret: bool | None = None
        self.is_feed_hooks: bool | None = None
        self.is_recording_hooks: bool | None = None
        self.is_thumbnail_hooks: bool | None = None
        self.is_transcoder_hooks: bool | None = None
        self.is_clip_hooks: bool | None = None

class CreateWebhook():
    """The :class:`CreateWebhook` object, which represents a Create webhook request."""

    def __init__(self, url: str, is_feed_hooks: bool, is_recording_hooks: bool):
        self.url = url
        self.is_feed_hooks = is_feed_hooks
        self.is_recording_hooks = is_recording_hooks
        self.is_thumbnail_hooks = False
        self.is_transcoder_hooks = False
        self.is_clip_hooks = False
