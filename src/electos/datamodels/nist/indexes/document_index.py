"""Indexes over models that return a context node."""

from electos.datamodels.nist.indexes.base import IndexBase


class DocumentIndex(IndexBase):

    """Index that returns model elements directly.

    It does not support mutating the contents after the index is created.
    """

    """Index that returns context nodes allowing modification of the document.

    Modification means being able to move or remove elements.
    """

    def _build_node(self, item, key, value):
        result = IndexNode(item, key, value)
        return result


class IndexNode:

    """Entry in the index describing an item and its container.

    Allows tracking the parent and key of an item so it can be moved or removed.
    """

    # Note: The field that stores the current item is `value`, *not* `parent`.

    def __init__(self, parent, key, value):
        """Create an index node.

        Parameters:
            parent: The container that holds the item with the value.
                It has one of the following types:
                - A mapping (a class defined in the JSON Schema)
                - A sequence (a list)
            key: The key used to get the value from the parent.
                If the parent is a mapping the key is the field name.
                If the parent is a sequence the key is a numeric index.
            value: The item being examined for reachability.
                Can be of any type.
        """
        self._parent = parent
        self._key = key
        self._value = value


    def __str__(self):
        """String form of the item.

        Note: This is not JSON.
        """
        return str(self._value)


    # Access to properties is read-only.

    @property
    def parent(self):
        """Item containing the value."""
        return self._parent


    @property
    def key(self):
        """Key (field name or index) used to access the value from the parent."""
        return self._key


    @property
    def value(self):
        """Item being examined for reachability."""
        return self._value
