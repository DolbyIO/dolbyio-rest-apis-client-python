"""
dolbyio_rest_apis.core.http_request_error
~~~~~~~~~~~~~~~

This module contains the model HttpRequestError.
"""

from aiohttp import ClientResponse

class HttpRequestError(Exception):
    r"""HTTP exception raised from a client request."""

    def __init__(self,
            http_response: ClientResponse,
            error_type: str,
            error_code: int,
            error_reason: str,
            error_description: str):
        self.status_code = http_response.status
        self.url = http_response.url
        self.error_type = error_type
        self.error_code = error_code
        self.error_reason = error_reason
        self.error_description = error_description

        super().__init__(error_description)

    def __str__(self) -> str:
        return f'''HTTP Request Error!\r
            \tURL: {self.url}\r
            \tStatus Code: {self.status_code}\r
            \tDolby.io Error Code:  {self.error_code}
            \tDolby.io Reason:      {self.error_reason}\r
            \tDolby.io Description: {self.error_description}'''
