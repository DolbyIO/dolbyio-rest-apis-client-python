"""
dolbyio_rest_apis.communications.internal.urls
~~~~~~~~~~~~~~~

This module contains the URLs to use to call the REST APIs.
"""

API_URL = 'api.dolby.io'
COMMS_URL = 'comms.api.dolby.io'
SESSION_URL = 'session.voxeet.com/v1'

def get_api_url() -> str:
    return f'https://{API_URL}/v1'

def get_monitor_url() -> str:
    return f'https://{COMMS_URL}/v1/monitor'

def get_comms_url_v2(region: str = None) -> str:
    if region is None:
        return f'https://{COMMS_URL}/v2'
    return f'https://{region}.{COMMS_URL}/v2'

def get_session_url() -> str:
    return f'https://{SESSION_URL}'
