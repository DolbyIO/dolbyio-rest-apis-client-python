"""
dolbyio_rest_apis.streaming.models.cluster
~~~~~~~~~~~~~~~

This module contains the models used by the Cluster module.
"""

from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json

@dataclass
class ClusterLocation:
    """The :class:`ClusterLocation` object, which represents the location of a cluster."""

    city: str | None = None
    region: str | None = None
    country: str | None = None

@dataclass
class ClusterFeatures:
    """The :class:`ClusterFeatures` object, which represents the available features of a cluster."""

    transcoding: bool = False

@dataclass
class Cluster:
    """The :class:`Cluster` object, which represents a cluster."""

    id: str
    name: str
    rtmp: str
    srt: str
    location: ClusterLocation
    features: ClusterFeatures

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ClusterResponse:
    """The :class:`ClusterResponse` object, which represents a cluster response."""

    default_cluster: str
    available_clusters: list[Cluster]
