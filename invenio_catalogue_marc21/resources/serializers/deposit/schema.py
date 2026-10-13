# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Schema for marc21 catalogue ui records."""

from flask_resources import BaseObjectSchema
from invenio_records_marc21.resources.serializers.deposit.schema import (
    MetadataDepositField,
)
from marshmallow.fields import Boolean, Dict, List, Method, Nested, String

from ..base import CatalogueSchema


def create_tree(root_id: str, parent_id: str, node: dict) -> dict:
    """Create Tree.

    it is used recursively
    """
    try:
        name = node["metadata"]["fields"]["245"][0]["subfields"]["a"]
    except KeyError:
        try:
            name = node["title"]
        except KeyError:
            name = "N/A"

    if "id" in node:
        pid = node["id"]
    elif "pid" in node:
        pid = node["pid"]

    return {
        "name": name,
        "node": pid,
        "self_html": f"/catalogue/uploads/{pid}",
        "root": root_id,
        "parent": parent_id,
        "children": [
            create_tree(root_id, pid, child) for child in node.get("children", [])
        ],
    }


class Marc21CatalogueDepositSchema(BaseObjectSchema):
    """Marc21 catalogue deposit schema."""

    id = String()
    links = Dict()
    metadata = MetadataDepositField()
    tree = Method(serialize="create_tree")
    is_catalogue = Boolean()
    files = Dict()
    access = Dict()
    catalogue = Nested(CatalogueSchema)
    children = List(Dict())

    def create_tree(self, obj: dict, **__: dict) -> dict:
        """Create tree."""
        return create_tree(obj["catalogue"]["root"], obj["catalogue"]["parent"], obj)
