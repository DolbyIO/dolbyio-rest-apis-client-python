"""
dolbyio_rest_apis.communications.internal.urls
~~~~~~~~~~~~~~~

This module contains the URLs to use to call the REST APIs.
"""

API_URL = 'https://api.voxeet.com'
SESSION_URL = 'https://session.voxeet.com/v1'

def get_api_v1_url() -> str:
    return f'{API_URL}/v1'

def get_api_v2_url() -> str:
    return f'{API_URL}/v2'

def get_monitor_url() -> str:
    return f'{get_api_v1_url()}/monitor'

def get_session_url() -> str:
    return SESSION_URL
