# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module link multiple marc21 modules."""

from invenio_drafts_resources.services.records.components import DraftFilesComponent
from invenio_rdm_records.services.components import AccessComponent
from invenio_records_marc21.services.components.metadata import MetadataComponent
from invenio_records_marc21.services.components.pid import PIDComponent
from invenio_records_marc21.services.components.pids import PIDsComponent

from .catalogue import CatalogueComponent

DefaultCatalogueComponents = [
    MetadataComponent,
    AccessComponent,
    DraftFilesComponent,
    PIDComponent,
    PIDsComponent,
    CatalogueComponent,
]

__all__ = (
    "CatalogueComponent",
    "DefaultCatalogueComponents",
)
