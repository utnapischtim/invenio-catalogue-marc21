# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue service component for ."""

from flask_principal import Identity
from invenio_drafts_resources.services.records import RecordService
from invenio_drafts_resources.services.records.components import ServiceComponent

from ...records.api import Marc21CatalogueDraft, Marc21CatalogueRecord


def update_parent(
    service: RecordService,
    record: Marc21CatalogueDraft | Marc21CatalogueRecord,
    identity: Identity,
) -> None:
    """Update parent."""
    parent_id = record.catalogue["parent"]
    id_ = record["id"]
    if not parent_id:
        return

    parent = service.edit(identity, parent_id)
    parent_data = parent.data

    if id_ in parent_data["catalogue"]["children"]:
        return

    title = record.metadata["fields"]["245"][0]["subfields"]["a"]
    for category in ["100", "700"]:
        try:
            authors = record.metadata["fields"][category][0]["subfields"]["a"]  # TODO
        except KeyError:
            authors = ""

    parent_data["catalogue"]["children"].append(id_)
    parent_data["children"].append(
        {  # this should be moved to a Schema, but with performance checks!
            "title": title,
            "authors": authors,
            "pid": id_,
        },
    )
    service.update_draft(
        identity=identity,
        id_=parent_id,
        data=parent_data,
    )


class CatalogueComponent(ServiceComponent):
    """Service component for Catalogue."""

    def create(  # type: ignore[override]
        self,
        identity: Identity,  # noqa: ARG002
        data: dict,
        record: Marc21CatalogueDraft | Marc21CatalogueRecord,
        errors: dict | None = None,  # noqa: ARG002
    ) -> None:
        """Create handler."""
        default_catalogue = {
            "root": record["id"],
            "parent": record["id"],
            "children": [],
        }

        record.catalogue = data.get("catalogue", default_catalogue)
        record.children = data.get("children", [])
        update_parent(self.service, record, identity)

    def update_draft(  # type: ignore[override]
        self,
        identity: Identity,  # noqa: ARG002
        data: dict,
        record: Marc21CatalogueDraft | Marc21CatalogueRecord,
        errors: dict | None = None,  # noqa: ARG002
    ) -> None:
        """Update draft handler."""
        record.catalogue = data.get("catalogue", {})
        record.children = data.get("children", [])
        update_parent(self.service, record, identity)

    def edit(
        self,
        identity: Identity,  # noqa: ARG002
        draft: Marc21CatalogueDraft | None = None,
        record: Marc21CatalogueRecord | None = None,
    ) -> None:
        """Edit a record handler."""
        if draft is None or record is None:
            return
        # TODO: check how the schema gets into the draft, because it is not there
        draft.catalogue = record.catalogue
        draft.children = record.children
        draft.bucket.locked = False  # to update files, which is by default not allowed!

    def publish(
        self,
        identity: Identity,  # noqa: ARG002
        draft: Marc21CatalogueDraft | None = None,
        record: Marc21CatalogueRecord | None = None,
    ) -> None:
        """Publish handler."""
        if draft is None or record is None:
            return
        record.catalogue = draft.catalogue
        record.children = draft.children
