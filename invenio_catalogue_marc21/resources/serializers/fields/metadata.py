# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""

from marshmallow.fields import Field


def field_controlfield(value: str, start: int = 0, end: int = -1) -> str:
    """MARC21 get sub string of a controlfields from json."""
    if isinstance(value, str):
        return value[start:end]
    return value


def field_subfields(value: list) -> list[dict]:
    """MARC21 get list of subfields from json."""
    subfields = []
    if isinstance(value, list):
        subfields = [field.get("subfields", {}) for field in value]
    return subfields


def field_subfield(key: str, subfields: dict) -> str:
    """Find subfield in a list of subfields dicts."""
    subfield = subfields.get(key, [])
    if isinstance(subfield, list):
        subfield = ", ".join(subfield)
    return subfield if subfield else ""


def make_affiliation_index(
    main_entry_personal_name: list,
    added_entry_personal_name: list,
) -> dict:
    """Make affiliation index."""
    creators = []
    affiliation_list = []

    affiliation_idx = {}
    index = {"val": 1}

    def _apply_idx(entry: dict) -> tuple[int, str]:
        name = field_subfield("4", entry)
        if name not in affiliation_idx:
            affiliation_idx[name] = index["val"]
            affiliation_list.append([index["val"], name])
            index["val"] += 1
        idx = affiliation_idx[name]
        return (idx, name)

    def _creator(entry: dict) -> dict:
        return {
            "person_or_org": {
                "type": "personal",
                "name": field_subfield("a", entry),
            },
            "affiliations": list(map(_apply_idx, [entry])),
        }

    creators = [
        _creator(entry)
        for entry in [*main_entry_personal_name, *added_entry_personal_name]
    ]

    return {
        "creators": creators,
        "affiliations": affiliation_list,
    }


class MetadataUIField(Field):
    """Schema for the record metadata."""

    def _serialize(
        self,
        value: dict,
        attr: str | None,  # noqa: ARG002
        obj: dict,  # noqa: ARG002
        **__: dict,
    ) -> dict:
        """Serialise access status."""
        fields = value.get("fields", {})
        out: dict = {}

        main_entry_personal_name = field_subfields(fields.get("100", []))
        title_statement = field_subfields(fields.get("245", []))
        added_entry_personal_name = field_subfields(fields.get("700", []))

        if main_entry_personal_name:
            out["main_entry_personal_name"] = {
                "personal_name": field_subfield("a", main_entry_personal_name[0]),
            }
        if added_entry_personal_name:
            out["added_entry_personal_name"] = [
                {"personal_name": field_subfield("a", creator)}
                for creator in added_entry_personal_name
            ]
        if title_statement:
            out["title_statement"] = {
                "title": field_subfield("a", title_statement[0]),
                "additional_title": field_subfield("b", title_statement[0]),
            }
            out["title"] = field_subfield("a", title_statement[0])

        out["creators"] = make_affiliation_index(
            main_entry_personal_name,
            added_entry_personal_name,
        )

        return out
