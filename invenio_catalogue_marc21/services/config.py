# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module link multiple marc21 modules."""

from invenio_records_marc21.services import Marc21RecordServiceConfig
from invenio_records_resources.services.base.config import FromConfig
from invenio_records_resources.services.records.results import RecordItem

from ..records import (
    Marc21CatalogueDraft,
    Marc21CatalogueRecord,
    Marc21CatalogueTasks,
)
from .components import DefaultCatalogueComponents
from .links import DefaultServiceLinks
from .schemas import Marc21CatalogueSchema


class Marc21CatalogueServiceConfig(Marc21RecordServiceConfig):  # type: ignore[misc]
    """Marc21 record service config."""

    record_cls = Marc21CatalogueRecord
    draft_cls = Marc21CatalogueDraft
    schema = Marc21CatalogueSchema

    result_item_cls = RecordItem
    schema_secret_link = None
    review = None

    links_item = FromConfig(
        "MARC21_RECORDS_SERVICE_LINKS",
        default=DefaultServiceLinks,
    )

    components = FromConfig(
        "MARC21_CATALOGUE_SERVICE_COMPONENTS",
        default=DefaultCatalogueComponents,
    )


class Marc21CatalogueTasksServiceConfig:
    """Config."""

    record_cls = Marc21CatalogueTasks
