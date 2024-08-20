"""
dolbyio_rest_apis.streaming.models.account
~~~~~~~~~~~~~~~

This module contains the models used by the Account module.
"""

from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AccountGeoCascade:
    """The :class:`AccountGeoCascade` object, the definition of the geo cascading rules for the account."""

    is_enabled: bool = False
    clusters: list[str] = field(default_factory=lambda: [])

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AccountGeoRestrictions:
    """The :class:`AccountGeoRestrictions` object, the definition of the geo restrictions rules for the account."""

    allowed_countries: list[str] = field(default_factory=lambda: [])
    denied_countries: list[str] = field(default_factory=lambda: [])
