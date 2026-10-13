# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Schemas for marc21 records serializers."""

from marshmallow import Schema
from marshmallow.fields import List, String


class CatalogueSchema(Schema):
    """Schema for a catalogue records."""

    root = String()
    parent = String()
    children = List(String())
