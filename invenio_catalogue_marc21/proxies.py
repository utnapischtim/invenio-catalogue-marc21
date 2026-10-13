# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Helper proxy to the state object."""

from typing import TYPE_CHECKING, cast

from flask import current_app
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    # i don't like it, but the only way, because of circular dependencies
    from .ext import InvenioCatalogueMarc21

current_catalogue_marc21: InvenioCatalogueMarc21 = cast(
    "InvenioCatalogueMarc21",
    LocalProxy(
        lambda: current_app.extensions["invenio-catalogue-marc21"],
    ),
)

"""Helper proxy to get the current records marc21 extension."""
