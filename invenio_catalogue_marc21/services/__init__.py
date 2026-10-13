# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module link multiple marc21 modules."""

from .config import Marc21CatalogueServiceConfig, Marc21CatalogueTasksServiceConfig
from .services import Marc21CatalogueService, Marc21CatalogueTasksService

__all__ = (
    "Marc21CatalogueService",
    "Marc21CatalogueServiceConfig",
    "Marc21CatalogueTasksService",
    "Marc21CatalogueTasksServiceConfig",
)
