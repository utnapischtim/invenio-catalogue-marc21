# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module link multiple marc21 modules."""

from .catalogue import CatalogueSchema, Marc21CatalogueSchema

__all__ = (
    "CatalogueSchema",
    "Marc21CatalogueSchema",
)
