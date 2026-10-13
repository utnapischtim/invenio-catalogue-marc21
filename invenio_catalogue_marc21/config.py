# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module link multiple marc21 modules."""

MARC21_CATALOGUE_BASE_TEMPLATE = "invenio_app_rdm/records/detail.html"
"""Default base template for the demo page."""


MARC21_CATALOGUE_UI_ENDPOINTS = {
    "record-detail": "/<pid_value>",
    "deposit-create": "/uploads/new",
    "deposit-edit": "/uploads/<pid_value>",
}
"""UI endpoints for invenio-catalogue-marc21."""

MARC21_CATALOGUE_JAVASCRIPT_EXTENDABLE: list[str] = []
"""Extend javascript."""

MARC21_CATALOGUE_IMPORT_CLS_TYPES: dict[str, str] = {}
"""Import clses."""
