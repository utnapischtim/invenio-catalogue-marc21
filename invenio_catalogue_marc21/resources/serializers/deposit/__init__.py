# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 Catalogue Deposit serializers module."""

from .schema import Marc21CatalogueDepositSchema
from .serializer import Marc21CatalogueDepositSerializer

__all__ = (
    "Marc21CatalogueDepositSchema",
    "Marc21CatalogueDepositSerializer",
)
