"""
dolbyio_rest_apis.core.helpers
~~~~~~~~~~~~~~~

This module contains some helpers.
"""

import enum

def get_value(value):
    return value.value if isinstance(value, enum.Enum) else value

def get_value_or_default(obj, name: str, default_value):
    return obj[name] if name in obj else default_value

def add_if_not_none(array, name: str, value):
    if not value is None:
        array[name] = get_value(value)

def in_and_not_none(dictionary, key):
    return key in dictionary and not dictionary[key] is None
