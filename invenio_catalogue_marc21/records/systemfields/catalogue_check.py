# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue status field.

The CatalogueCheckField is used to check if an associated PID is in a given state.
For instance:

.. code-block:: python

    class Record():
        catalogue = CatalogueField()
        is_catalogue = CatalogueCheckField('catalogue')

"""

from typing import TYPE_CHECKING, Any, Self, overload

from invenio_records.dictutils import dict_lookup, dict_set, parse_lookup_key
from invenio_records.systemfields import SystemField

# this is not working at the moment, since there is a circular dependency flow
# from ..api import Marc21CatalogueDraft, Marc21CatalogueRecord # noqa: ERA001
# this is not working at runtime since SystemField is not subscriptable
# class CatalogueCheckField(SystemField[Marc21CatalogueRecord | Marc21CatalogueDraft]):

if TYPE_CHECKING:
    from ..api import Marc21CatalogueDraft, Marc21CatalogueRecord


class CatalogueCheckField(SystemField):
    """PID status field which checks against an expected status.

    The `CatalogueCheckField` class is a system field in the context of
    Invenio-Records-Resources that is used to check the presence of a catalogue
    attribute in a record. It is designed to be used for checking if a specific
    attribute (in this case, a catalogue) exists in a record and returns a
    boolean value based on its presence.
    """

    def __init__(
        self,
        key: str = "catalogue",
        value: str = "",  # noqa: ARG002
        *,
        dump: bool = False,
    ) -> None:
        """Initialize the CatalogueField.

        :param key: Attribute name of the CatalogueField to use for status check.
        :param status: The status or list of statuses which will return true.
        :param dump: Dump the status check in the index. Default to False.
        """
        super().__init__(key=key)
        self._dump = dump

    #
    # Data descriptor methods (i.e. attribute access)
    #
    @overload
    def __get__(
        self,
        record: None,
        owner: type[Marc21CatalogueRecord | Marc21CatalogueDraft] | None = None,
    ) -> Self: ...

    @overload
    def __get__(
        self,
        record: Marc21CatalogueRecord | Marc21CatalogueDraft,
        owner: type[Marc21CatalogueRecord | Marc21CatalogueDraft] | None = None,
    ) -> bool: ...

    def __get__(
        self,
        record: Marc21CatalogueRecord | Marc21CatalogueDraft | None,
        owner: type[Marc21CatalogueRecord | Marc21CatalogueDraft] | None = None,
    ) -> bool | Self:
        """Get the persistent identifier."""
        if record is None:
            return self  # returns the field itself.
        catalogue = getattr(record, self.key)
        return bool(catalogue)

    def pre_dump(
        self,
        record: Marc21CatalogueRecord | Marc21CatalogueDraft,
        data: dict[str, Any],
        dumper: Any | None = None,
    ) -> None:
        """Called before a record is dumped in a secondary storage system."""
        if self._dump:
            dict_set(data, self.attr_name, getattr(record, self.attr_name))

    def pre_load(self, data: dict[str, Any], loader: Any | None = None) -> None:
        """Called before a record is dumped in a secondary storage system."""
        if self._dump:
            keys = parse_lookup_key(self.attr_name)
            parent = dict_lookup(data, keys, parent=True)
            parent.pop(keys[-1], None)
