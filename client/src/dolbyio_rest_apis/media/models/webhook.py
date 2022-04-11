"""
dolbyio_rest_apis.media.models.webhook
~~~~~~~~~~~~~~~

This module contains the Webhook model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default

class Webhook(dict):
    """The :class:`Webhook` object, which represents a webhook."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.webhook_id = get_value_or_default(self, 'webhook_id', None)
        self.url = None
        self.headers = None
        if 'callback' in self:
            callback = self['callback']
            self.url = get_value_or_default(callback, 'url', None)
            self.headers = get_value_or_default(callback, 'headers', None)
