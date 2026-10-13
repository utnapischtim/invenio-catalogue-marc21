# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module link multiple marc21 modules."""

from invenio_records_marc21.services.schemas import Marc21RecordSchema
from marshmallow import Schema
from marshmallow.fields import Dict, List, Str
from marshmallow_utils.fields import NestedAttribute


class CatalogueSchema(Schema):
    """Catalogue schema."""

    parent = Str(required=True)
    root = Str(required=True)
    children = List(Str())


class Marc21CatalogueSchema(Marc21RecordSchema):  # type: ignore[misc]
    """Marc21CatalogueSchema."""

    catalogue = NestedAttribute(CatalogueSchema)
    children = List(Dict())
