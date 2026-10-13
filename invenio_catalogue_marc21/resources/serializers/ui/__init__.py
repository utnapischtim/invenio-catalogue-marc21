# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 Resources serializers module."""

from .schema import Marc21CatalogueUISchema
from .serializer import Marc21CatalogueUIJSONSerializer

__all__ = (
    "Marc21CatalogueUIJSONSerializer",
    "Marc21CatalogueUISchema",
)
