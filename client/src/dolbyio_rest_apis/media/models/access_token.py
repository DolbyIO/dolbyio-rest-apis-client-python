"""
dolbyio_rest_apis.media.models.access_token
~~~~~~~~~~~~~~~

This module contains the models used by the Access Token model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default

class AccessToken(dict):
    """The :class:`AccessToken` object, which represents the access token."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.token_type = get_value_or_default(self, 'token_type', None)
        self.access_token = get_value_or_default(self, 'access_token', None)
        self.expires_in_val = get_value_or_default(self, 'expires_in', 0)
        self.status = get_value_or_default(self, 'status', None)
