# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 Resources serializers module."""

from .base import CatalogueSchema
from .deposit import Marc21CatalogueDepositSerializer
from .ui import Marc21CatalogueUIJSONSerializer

__all__ = (
    "Marc21CatalogueDepositSerializer",
    "CatalogueSchema",
    "Marc21CatalogueUIJSONSerializer",
)
