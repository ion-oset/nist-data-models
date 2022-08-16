"""Indexes over models that return elements directly."""

from electos.datamodels.nist.indexes.base import IndexBase


class ElementIndex(IndexBase):

    """Index that returns model elements directly.

    It does not support mutating the contents after the index is created.
    """

    def _build_node(self, item, key, value):
        result = value
        return result
