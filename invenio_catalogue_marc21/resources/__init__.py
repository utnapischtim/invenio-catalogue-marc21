# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Catalogue service component for ."""

from .config import (
    Marc21CatalogueAlmaProxyResourceConfig,
    Marc21CatalogueRecordResourceConfig,
    Marc21CatalogueResourceConfig,
    Marc21CatalogueTasksConfig,
)
from .resources import (
    Marc21CatalogueAlmaProxyResource,
    Marc21CatalogueRecordResource,
    Marc21CatalogueResource,
    Marc21CatalogueTasksResource,
)

__all__ = (
    "Marc21CatalogueAlmaProxyResource",
    "Marc21CatalogueAlmaProxyResourceConfig",
    "Marc21CatalogueRecordResource",
    "Marc21CatalogueRecordResourceConfig",
    "Marc21CatalogueResource",
    "Marc21CatalogueResourceConfig",
    "Marc21CatalogueTasksConfig",
    "Marc21CatalogueTasksResource",
)
