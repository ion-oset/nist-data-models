"""Base class of indexes over models."""

from abc import ABCMeta, abstractmethod
from collections.abc import Sequence, Mapping

from electos.datamodels.nist.models.base import NistModel


class IndexBase(metaclass = ABCMeta):

    """Abstract base class for indexes: fast access to elements in a model.

    Currently provides a limited DOM-like interface by '@id' and '@type'.
    Only elements (mappings) are indexed: Lists and scalars have no
    '@id' or '@type'.

    Note: This is an *abstract class*. Subclasses should override build indexes.
    """

    def __init__(self, document, namespace):
        """Create an index.

        Parameters:
            document: Nested tree of model elements.
            namespace: The namespace prefix attached to element types, if any.
                This parameter is deliberately not optional to avoid forgetting
                to set it. If there is no namespace use "".
        """
        # Document to index
        self._document = document
        # Namespace prefix
        self._namespace = namespace
        # Index of elements by '@id'
        self._by_id = {}
        # Index of elements by '@type'
        self._by_type = {}
        # Generate the indexes
        self._build_indexes()


    # --- IDs

    def ids(self):
        """Access all element type IDs.

        The order is the same order they are encountered in the document.
        Each ID must be unique.

        Yields:
            The id of each element in the document that has one.
        """
        for name in self._by_id:
            yield name


    def by_id(self, id, strict = False):
        """Access element whose '@id' is 'id'.

        Parameters:
            id: Model ID to look up.
            strict: Force an exception if the model ID is not found.

        Returns:
            The element associated with the model ID.
            None, if the ID is not found and 'strict' is false.

        Raises:
            KeyError if the ID is not found and 'strict' is true.
        """
        id_ = id
        item = self._by_id.get(id_, None)
        if not item and strict:
            raise KeyError(f"No item in index with '@id': {id_}")
        return item


    # --- Types

    def types(self, with_namespace = True):
        """Access all element type names.

        Each type name only appears once in the order they are first encountered
        in the document.

        Yields:
            The type names of elements found in the document.
        """
        for name in self._by_type:
            yield name if with_namespace else name[len(self._namespace) + 1:]


    def by_type(self, type, strict = False):
        """Access all elements whose '@type' is 'type'.

        Parameters:
            type: Model type to look up.
            strict: Force an exception if the model type is not found.
            with_namespace: True if the schema namespace prefix is required.
                Otherwise prepend the namespace to all type names for lookup.

        Yields: Each element with the given type.
            The order of the elements in the model is preserved.

        Raises:
            KeyError if the ID is not found and 'strict' is true.
        """
        type_ = type
        if "." not in type_:
            type_ = f"{self._namespace}.{type_}"
        items = self._by_type.get(type_, [])
        if not items and strict:
            raise KeyError(f"No items in index with '@type': {type_}")
        for item in items:
            yield item


    # --- Internal interface

    def _build_indexes(self):
        """Build the ID and type indexes."""
        for item, key, value in self._walk_document(self._document):
            if not isinstance(value, NistModel):
                continue
            node = self._build_node(item, key, value)
            if hasattr(value, "model__id"):
                self._by_id[value.model__id] = node
            if hasattr(value, "model__type"):
                self._by_type.setdefault(value.model__type, []).append(node)


    @abstractmethod
    def _build_node(self, item, key, value):
        """Create node that is returned by an index lookup on the key."""
        pass


    def _walk_document(self, parent):
        """Walk all objects in a document, depth first.

        Yields the objects, their parents, and their keys, to allow basic
        mutations of the document tree at each step.

        Parameters:
            parent: The object being walked.

        Yields:
            parent: Parent item of the value
            - For a mapping or sequence: the input 'parent'.
            - For a scalar: None
            key: The key used to access the value.
            - For a mapping: key
            - For a sequence: numeric index
            - For a scalar: None
            value: The value.
            - For a mapping or sequence: 'parent[key]'
            - For a scalar: the 'parent'
        """
        assert not isinstance(parent, Mapping), \
              f"There should be no mappings in a model: {parent}\n" \
              "Did you start indexing from a dictionary instead of a model?"
        if isinstance(parent, NistModel):
            for name in parent.__fields__.keys():
                value = getattr(parent, name)
                yield parent, name, value
                yield from self._walk_document(value)
        elif isinstance(parent, Sequence) and not isinstance(parent, (str, bytes)):
            for index, value in enumerate(parent):
                yield parent, index, value
                yield from self._walk_document(value)
        else:
            parent, key, value = None, None, parent
            yield parent, key, value
