# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service links."""

from collections.abc import Callable

from invenio_drafts_resources.services.records.config import is_draft, is_record
from invenio_records_marc21.services.links import record_doi_link
from invenio_records_resources.records import Record
from invenio_records_resources.services import ConditionalLink
from invenio_records_resources.services.records.links import RecordEndpointLink


class SwitchLinks:
    """Switch link."""

    def __init__(
        self,
        cond: list[
            tuple[Callable[[Record, dict], bool], ConditionalLink | RecordEndpointLink]
        ],
    ) -> None:
        """Construct."""
        # conditions are a tuple of 1: is the condition and 2: the template
        self._conditions = cond

    def should_render(self, obj: Record, ctx: dict) -> bool:
        """Determine if the link should be rendered."""
        for condition, template in self._conditions:
            if condition(obj, ctx):
                return template.should_render(obj, ctx)
        return False

    def expand(self, obj: Record, ctx: dict) -> str | None:
        """Determine if the link should be rendered."""
        for condition, template in self._conditions:
            if condition(obj, ctx):
                return template.expand(obj, ctx)
        return None


def is_catalogue(record: Record, _: dict) -> bool:
    """Shortcut for links to determine if record is a catalogue record."""
    return "marc21-catalogue" in record.get("$schema", "")


def is_base_marc21_record(record: Record, ctx: dict) -> bool:
    """Shortcut for links to determine if a record is a base marc21 record."""
    # TODO!!!!!!!!
    # this is only a shortcut. it should be implemented more directly
    return not is_catalogue(record, ctx)


DefaultServiceLinks = {
    "self": SwitchLinks(
        cond=[
            (
                is_catalogue,
                ConditionalLink(
                    cond=is_record,
                    if_=RecordEndpointLink(
                        "marc21_catalogue_records.read",
                        params=["pid_value", "key"],
                    ),
                    else_=RecordEndpointLink(
                        "marc21_catalogue_records.read_draft",
                        params=["pid_value", "key"],
                    ),
                ),
            ),
            (
                is_base_marc21_record,
                ConditionalLink(
                    cond=is_record,
                    if_=RecordEndpointLink("marc21_records.read"),
                    else_=RecordEndpointLink("marc21_records.read_draft"),
                ),
            ),
        ],
    ),
    "self_html": SwitchLinks(
        cond=[
            (
                is_catalogue,
                ConditionalLink(
                    cond=is_record,
                    if_=RecordEndpointLink("invenio_catalogue_marc21.record_detail"),
                    else_=RecordEndpointLink("invenio_catalogue_marc21.deposit_edit"),
                ),
            ),
            (
                is_base_marc21_record,
                ConditionalLink(
                    cond=is_record,
                    if_=RecordEndpointLink("invenio_records_marc21.record_detail"),
                    else_=RecordEndpointLink("invenio_records_marc21.deposit_edit"),
                ),
            ),
        ],
    ),
    "self_doi": record_doi_link,
    "doi": record_doi_link,
    "files": ConditionalLink(
        cond=is_record,
        if_=RecordEndpointLink("marc21_record_files.search"),
        else_=RecordEndpointLink("marc21_draft_files.search"),
    ),
    "draft": SwitchLinks(
        cond=[
            (
                is_catalogue,
                RecordEndpointLink(
                    "invenio_catalogue_marc21.deposit_edit",
                    when=is_record,
                ),
            ),
            (
                is_base_marc21_record,
                RecordEndpointLink(
                    "invenio_records_marc21.deposit_edit",
                    when=is_record,
                ),
            ),
        ],
    ),
    "edit": SwitchLinks(
        cond=[
            (
                is_catalogue,
                RecordEndpointLink("marc21_catalogue_records.edit"),
            ),
            (
                is_base_marc21_record,
                RecordEndpointLink("marc21_records.edit"),
            ),
        ],
    ),
    "publish": SwitchLinks(
        cond=[
            (
                is_catalogue,
                RecordEndpointLink("marc21_catalogue_records.publish", when=is_draft),
            ),
            (
                is_base_marc21_record,
                RecordEndpointLink("marc21_records.publish", when=is_draft),
            ),
        ],
    ),
    "catalogue": SwitchLinks(
        cond=[
            (
                is_catalogue,
                RecordEndpointLink("marc21_catalogue.catalogue", params=["pid_value"]),
            ),
        ],
    ),
}
