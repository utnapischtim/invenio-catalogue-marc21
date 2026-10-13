# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module link multiple marc21 modules."""

from typing import cast

from flask import Blueprint, Flask

from .ext import InvenioCatalogueMarc21


def create_record_bp(app: Flask) -> Blueprint:
    """Create records blueprint."""
    ext = cast(InvenioCatalogueMarc21, app.extensions["invenio-catalogue-marc21"])
    return ext.record_resource.as_blueprint()


def create_catalogue_bp(app: Flask) -> Blueprint:
    """Create records blueprint."""
    ext = cast(InvenioCatalogueMarc21, app.extensions["invenio-catalogue-marc21"])
    return ext.record_catalgoue.as_blueprint()


def create_alma_proxy_bp(app: Flask) -> Blueprint:
    """Create proxy blueprint."""
    ext = cast(InvenioCatalogueMarc21, app.extensions["invenio-catalogue-marc21"])
    return ext.alma_proxy.as_blueprint()


def create_tasks_bp(app: Flask) -> Blueprint:
    """Create tasks blueprint."""
    ext = cast(InvenioCatalogueMarc21, app.extensions["invenio-catalogue-marc21"])
    return ext.tasks_resource.as_blueprint()
