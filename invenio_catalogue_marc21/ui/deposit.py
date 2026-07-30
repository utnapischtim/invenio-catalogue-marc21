# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 records deposit backend."""

from flask import current_app, g
from invenio_i18n.proxies import current_i18n
from invenio_records_marc21.proxies import current_records_marc21


def deposit_templates() -> list:
    """Retrieve from DB the tamplates for marc21 deposit form."""
    templates = current_records_marc21.templates_service.get_templates(g.identity)

    if templates:
        return [template.to_dict() for template in templates]

    return []


def deposit_config(api_url: str = "") -> dict:
    """Create an deposit configuration."""
    app_config = current_app.config
    jsonschema = current_app.extensions["invenio-jsonschemas"]
    schema = {}

    if jsonschema:
        schema = jsonschema.get_schema(path="marc21/marc21-structure-v1.0.0.json")

    config = {
        "current_locale": str(current_i18n.locale),
        "default_locale": app_config.get("BABEL_DEFAULT_LOCALE", "en"),
        "error": "",
        "schema": schema,
        "quota": app_config.get("APP_RDM_DEPOSIT_FORM_QUOTA"),
        "createUrl": "/api/catalogue",
        "apiHeaders": app_config.get("MARC21_API_HEADERS"),
        # UploadFilesToolbar disable file upload
        "canHaveMetadataOnlyRecords": True,
    }

    if api_url:
        config["apiUrl"] = api_url

    return config
