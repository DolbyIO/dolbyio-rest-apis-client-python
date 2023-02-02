"""
dolbyio_rest_apis.streaming.models.cluster
~~~~~~~~~~~~~~~

This module contains the models used by the Cluster model.
"""

from dolbyio_rest_apis.core.helpers import get_value_or_default

class Cluster(dict):
    """The :class:`Cluster` object, which represents a cluster."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.id = get_value_or_default(self, 'id', None)
        self.name = get_value_or_default(self, 'name', None)
        self.rtmp = get_value_or_default(self, 'rtmp', None)

class ClusterResponse(dict):
    """The :class:`ClusterResponse` object, which represents a cluster response."""

    def __init__(self, dictionary: dict):
        dict.__init__(self, dictionary)

        self.default_cluster = get_value_or_default(self, 'defaultCluster', None)
        self.available_clusters = []
        for cluster in self['availableClusters']:
            self.available_clusters.append(Cluster(cluster))
