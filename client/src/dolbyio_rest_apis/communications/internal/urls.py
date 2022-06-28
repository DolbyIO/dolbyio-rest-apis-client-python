"""
dolbyio_rest_apis.communications.internal.urls
~~~~~~~~~~~~~~~

This module contains the URLs to use to call the REST APIs.
"""

API_URL = 'https://api.voxeet.com'
COMMS_URL = 'https://comms.api.dolby.io'
SESSION_URL = 'https://session.voxeet.com/v1'

def get_api_url() -> str:
    return f'{API_URL}/v1'

def get_monitor_url() -> str:
    return f'{COMMS_URL}/v1/monitor'

def get_comms_url_v2() -> str:
    return f'{COMMS_URL}/v2'

def get_session_url() -> str:
    return SESSION_URL
