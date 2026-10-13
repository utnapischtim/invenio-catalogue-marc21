# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Models."""

from invenio_db import db
from invenio_records.models import RecordMetadataBase


class Marc21CatalogueTasksMetadata(db.Model, RecordMetadataBase):  # type: ignore[name-defined, misc]
    """Marc21 catalogue progress metadata."""

    __tablename__ = "marc21_catalogue_tasks"
