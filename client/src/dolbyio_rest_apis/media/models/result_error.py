"""
dolbyio_rest_apis.media.models.result_error
~~~~~~~~~~~~~~~

This module contains the Result Error model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default

class ResultError(dict):
    """The :class:`ResultError` object, which represents an enhance job error."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.type = get_value_or_default(self, 'type', None)
        self.title = get_value_or_default(self, 'title', None)
        self.detail = get_value_or_default(self, 'detail', None)
