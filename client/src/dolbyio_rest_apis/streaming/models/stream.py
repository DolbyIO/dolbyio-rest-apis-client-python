"""
dolbyio_rest_apis.streaming.models.stream
~~~~~~~~~~~~~~~

This module contains the models used by the Stream module.
"""

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StreamStoppingLevel:
    """The :class:`StreamStoppingLevel` object, which represents the response to stopping a stream."""

    stopping_level: str
