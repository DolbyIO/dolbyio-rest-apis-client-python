"""
dolbyio_rest_apis.media.models.paged_response
~~~~~~~~~~~~~~~

This module contains the Paged Response base model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default

class PagedResponse(dict):
    r"""Representation of a paged response."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.next_token = get_value_or_default(self, 'next_token', None)
        self.count = get_value_or_default(self, 'count', None)
