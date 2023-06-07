"""
dolbyio_rest_apis.communications.models
~~~~~~~~~~~~~~~

This module contains the models used by the Dolby.io APIs.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default

class AccessToken(dict):
    """The :class:`AccessToken` object, which represents the access token."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.token_type = get_value_or_default(self, 'token_type', None)
        self.access_token = get_value_or_default(self, 'access_token', None)
        self.refresh_token = get_value_or_default(self, 'refresh_token', None)
        self.expires_in_val = get_value_or_default(self, 'expires_in', 0)
        self.scope = get_value_or_default(self, 'scope', None)
