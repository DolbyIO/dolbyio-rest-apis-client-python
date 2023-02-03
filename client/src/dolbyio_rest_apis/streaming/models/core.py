"""
dolbyio_rest_apis.streaming.models.core
~~~~~~~~~~~~~~~
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default

class BaseResponse(dict):
    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.status = get_value_or_default(self, 'status', None)
        self.data = get_value_or_default(self, 'data', None)

class Error(dict):
    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.message = get_value_or_default(self, 'message', None)
