# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Deserializers."""

from flask_resources import BaseObjectSchema
from marshmallow import pre_load
from marshmallow.fields import Boolean, Dict, List, Nested
from marshmallow_utils.fields import Method, SanitizedUnicode

from ..serializers import CatalogueSchema


class Marc21DeserializeSchema(BaseObjectSchema):
    """Marc21DeserializeSchema."""

    id = SanitizedUnicode()
    catalogue = Nested(CatalogueSchema)
    is_catalogue = Boolean()
    metadata = Method(deserialize="load_metadata")
    children = List(Dict())
    links = Dict()
    files = Dict()
    access = Dict()

    @pre_load
    def skip(self, data: dict, **__: dict) -> dict:
        """Skip."""
        del data["tree"]
        return data

    def load_metadata(self, data: dict) -> dict:
        """Load metadata.

        Converts the list flat structure to dict structure.
        [
            {
                "id": "007",
                "ind1": " ",
                "ind2": " ",
                "subfield": "cr#|||||||||||"
           },
           {
                "id": "245",
                "ind1": "1",
                "ind2": "0",
                "subfield": "$$a Lorem Ipsum $$o 2025"
           }
        ]

        to

        {
            "007": "cr#|||||||||||"
            "245": {
                "ind1": "1",
                "ind2": "0",
                "subfields": {
                    "a": "Lorem Ipsum",
                    "o": "2025"
                }
            }
        }
        """
        fields = {}

        # all below of 10 is a control_number in marc21
        control_number_max = 10

        for field in data["fields"]:
            if int(field["id"]) < control_number_max:
                fields[field["id"]] = field["subfield"]
            else:
                if field["id"] not in fields:
                    fields[field["id"]] = []

                subfields = {
                    v[0:1]: [v[2:].strip()] for v in field["subfield"].split("$$")[1:]
                }

                fields[field["id"]].append(
                    {
                        "ind1": field["ind1"],
                        "ind2": field["ind2"],
                        "subfields": subfields,
                    },
                )
        return {
            "fields": fields,
            "leader": data["leader"],
        }
