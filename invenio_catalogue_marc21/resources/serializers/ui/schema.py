# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Schema for marc21 catalogue ui records."""

from functools import partial

from flask_resources import BaseObjectSchema
from invenio_i18n import get_locale
from invenio_rdm_records.resources.serializers.ui.fields import AccessStatusField
from marshmallow import post_dump
from marshmallow_utils.fields import FormatDate as BaseFormatDatetime
from marshmallow_utils.fields import SanitizedUnicode

from ..fields import MetadataUIField

FormatDatetime = partial(BaseFormatDatetime, locale=get_locale)


class Marc21CatalogueUISchema(BaseObjectSchema):
    """Schema for dumping extra information for the UI."""

    object_key = "ui"

    additional = (
        "status",
        "links",
    )

    id = SanitizedUnicode()

    access_status = AccessStatusField(attribute="access", dump_only=True)

    metadata = MetadataUIField()

    created = FormatDatetime(format="long")

    updated = FormatDatetime(format="long")

    @post_dump
    def creators(self, obj: dict, **__: dict) -> dict:
        """Creators post dump."""
        # the only way to apply metadata to creators too
        obj["creators"] = obj["metadata"]["creators"]
        return obj
