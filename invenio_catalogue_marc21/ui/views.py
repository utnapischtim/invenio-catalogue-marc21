# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""

from typing import cast

from flask import current_app, g, render_template
from flask_login import login_required
from invenio_records_resources.services.files.results import FileItem
from invenio_records_resources.services.records import RecordService
from invenio_records_resources.services.records.results import RecordItem
from invenio_stats.proxies import current_stats

from ..proxies import current_catalogue_marc21
from ..records.api import Marc21CatalogueRecord
from ..resources.serializers import (
    Marc21CatalogueDepositSerializer,
    Marc21CatalogueUIJSONSerializer,
)
from .decorators import (
    pass_draft,
    pass_draft_files,
    pass_record_files,
    pass_record_or_draft,
)
from .deposit import deposit_config


def _service() -> RecordService:
    """Get the record service."""
    return current_catalogue_marc21.records_service


def empty_record() -> dict:
    """Create an empty record."""
    record = {
        "id": "",
        "links": {},
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": [],
        },
        "tree": {
            "name": ["N/A"],
            "node": "",
            "self_html": "",
            "root": "",
            "parent": "",
            "children": [],
        },
        "files": {
            "enabled": True,
        },
        "access": {
            "record": "public",
            "files": "public",
        },
        "catalogue": {
            "root": "",
            "parent": "",
            "children": [],
        },
        "children": [],
    }

    return record


def calculate_root(pid: str) -> dict:
    """Calculate root."""
    if pid == "":
        title = ""
    else:
        root = _service().read(g.identity, pid)
        title = root._record.metadata["fields"]["245"][0]["subfields"]["a"][0]

    return {"pid": pid, "title": title}


def calculate_parent(pid: str) -> dict:
    """Calculate parent."""
    if pid == "":
        title = ""
    else:
        parent = _service().read(g.identity, pid)
        title = parent._record.metadata["fields"]["245"][0]["subfields"]["a"][0]
    return {"pid": pid, "title": title}


@pass_record_or_draft
@pass_record_files
def record_detail(
    record: RecordItem,
    files: FileItem,
    pid_value: str,
    *,
    is_preview: bool = False,
) -> str:
    """Record detail page (aka landing page)."""
    files_dict = files.to_dict() if files else {}

    emitter = current_stats.get_event_emitter("marc21-record-view")
    if record is not None and emitter is not None:
        emitter(current_app, record=record._record, via_api=False)

    _record = cast(Marc21CatalogueRecord, record._record)

    root = calculate_root(_record.catalogue["root"])
    parent = calculate_parent(_record.catalogue["parent"])

    children = _record.children
    serializer = Marc21CatalogueUIJSONSerializer()
    record_ui = serializer.dump_obj(record.to_dict())

    # ATTENTION:
    # this one is a quick and dirty fix
    # it should be done in the schema somehow, but since in my point of view
    # rdm-records makes it more complicated as necessary i will leave it like
    # that for the moment
    record_ui["metadata"] = record_ui["ui"]["metadata"]

    return render_template(
        "invenio_catalogue_marc21/landing_page/record.html",
        record=record,
        record_ui=record_ui,
        pid=pid_value,
        files=files_dict,
        permissions=record.has_permissions_to(
            ["edit", "new_version", "manage", "update_draft", "read_files"],
        ),
        children=children,
        parent=parent,
        root=root,
        is_preview=is_preview,
        is_draft=_record.is_draft,
    )


@login_required
def deposit_create() -> str:
    """Create a new deposit page."""
    # TODO: checkout to in deposit_edit
    # the permission system has to be established yet
    permissions = {
        "showMetadataAccess": False,
        "showFileAccess": False,
        "showFileUploader": True,
        "showImportFromAlma": True,
        "showUploadCSV": True,
    }

    # needed that the expandable works!
    expand_javascript = current_app.config.get(
        "MARC21_CATALOGUE_JAVASCRIPT_EXTENDABLE",
        [],
    )

    return render_template(
        "invenio_catalogue_marc21/deposit/index.html",
        forms_config=deposit_config(),
        record=empty_record(),
        files={"default_preview": None, "entries": [], "links": {}},
        permissions=permissions,
        expand_javascript=expand_javascript,
        # templates=deposit_templates(),
    )


@login_required
@pass_draft
@pass_draft_files
def deposit_edit(
    draft: RecordItem,
    draft_files: FileItem,
    pid_value: str,
) -> str:
    """Edit an existing deposit."""
    serializer = Marc21CatalogueDepositSerializer()
    serialized_record = serializer.dump_obj(draft.to_dict())

    permissions = draft.has_permissions_to(
        [
            "new_version",
            "showMetadataAccess",
            "showFileAccess",
            "showFileUploader",
            "showImportFromAlma",
        ],
    )

    # TODO: should be clearly temporarly ;)
    permissions["showImportFromAlma"] = True
    permissions["showFileUploader"] = True
    permissions["showUploadCSV"] = True

    # needed that the expandable works!
    expand_javascript = current_app.config.get(
        "MARC21_CATALOGUE_JAVASCRIPT_EXTENDABLE",
        [],
    )

    return render_template(
        "invenio_catalogue_marc21/deposit/index.html",
        forms_config=deposit_config(api_url=f"/api/catalogue/{pid_value}/draft"),
        record=serialized_record,
        files=draft_files.to_dict(),
        permissions=permissions,
        expand_javascript=expand_javascript,
    )
