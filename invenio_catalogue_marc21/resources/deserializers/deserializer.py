# -*- coding: utf-8 -*-
#
# Copyright (C) 2025-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Deserializers."""

from flask_resources import JSONDeserializer
from marshmallow_utils.context import context_schema

from .schema import Marc21DeserializeSchema


class Marc21CatalogueDeserializer(JSONDeserializer):
    """Marc21 json deserializer."""

    def __init__(self, schema: type = Marc21DeserializeSchema) -> None:
        """Deserializer initialization."""
        self.schema = schema

    def deserialize(self, data: str | bytes | bytearray | memoryview | None) -> None:
        """Deserialize."""
        deserialized_data = super().deserialize(data)

        def _permission_check(*_: dict, **__: dict) -> bool:
            return True

        token = context_schema.set({"field_permission_check": _permission_check})

        schema = self.schema()

        try:
            return schema.load(deserialized_data)
        finally:
            context_schema.reset(token)
