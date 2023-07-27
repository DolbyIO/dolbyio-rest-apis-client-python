"""
dolbyio_rest_apis.core.urls
~~~~~~~~~~~~~~~

This module contains the URLs to use to call the REST APIs.
"""

API_URL = 'api.dolby.io'
COMMS_URL = 'comms.api.dolby.io'
SAPI_URL = 'api.millicast.com'
MAPI_URL = 'api.dolby.com'

def get_api_url() -> str:
    return f'https://{API_URL}/v1'

def get_comms_url_v1() -> str:
    return f'https://{COMMS_URL}/v1'

def get_comms_url_v2(region: str = None) -> str:
    if region is None:
        return f'https://{COMMS_URL}/v2'
    return f'https://{region}.{COMMS_URL}/v2'

def get_comms_monitor_url_v1() -> str:
    return f'{get_comms_url_v1()}/monitor'

def get_comms_monitor_url_v2() -> str:
    return f'{get_comms_url_v2()}/monitor'

def get_rts_url() -> str:
    return f'https://{SAPI_URL}'

def get_mapi_url() -> str:
    return f'https://{MAPI_URL}'
