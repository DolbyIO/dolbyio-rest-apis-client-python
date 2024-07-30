"""
dolbyio_rest_apis.core.urls
~~~~~~~~~~~~~~~

This module contains the URLs to use to call the REST APIs.
"""

API_URL = 'api.dolby.io'
SAPI_URL = 'api.millicast.com'
MAPI_URL = 'api.dolby.com'

def get_api_url() -> str:
    return f'https://{API_URL}/v1'

def get_rts_url() -> str:
    return f'https://{SAPI_URL}'

def get_mapi_url() -> str:
    return f'https://{MAPI_URL}'
