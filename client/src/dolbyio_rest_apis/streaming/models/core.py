"""
dolbyio_rest_apis.streaming.models.core
~~~~~~~~~~~~~~~
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BaseResponse():
    status: str
    data: dict | list[dict]

@dataclass_json
@dataclass
class Error:
    message: str
