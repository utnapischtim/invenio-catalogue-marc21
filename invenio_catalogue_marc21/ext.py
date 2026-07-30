# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""

from flask import Flask
from invenio_rdm_records.services.pids import PIDManager, PIDsService
from invenio_records_marc21.services import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
)
from invenio_records_resources.services import FileService

from . import config
from .resources import (
    Marc21CatalogueAlmaProxyResource,
    Marc21CatalogueAlmaProxyResourceConfig,
    Marc21CatalogueRecordResource,
    Marc21CatalogueRecordResourceConfig,
    Marc21CatalogueResource,
    Marc21CatalogueResourceConfig,
    Marc21CatalogueTasksConfig,
    Marc21CatalogueTasksResource,
)
from .services import (
    Marc21CatalogueService,
    Marc21CatalogueServiceConfig,
    Marc21CatalogueTasksService,
    Marc21CatalogueTasksServiceConfig,
)


class InvenioCatalogueMarc21:
    """invenio-catalogue-marc21 extension."""

    def __init__(self, app: Flask | None = None) -> None:
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resources()
        app.extensions["invenio-catalogue-marc21"] = self

    def init_config(self, app: Flask) -> None:
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        for k in dir(config):
            if k.startswith("MARC21_CATALOGUE_"):
                app.config.setdefault(k, getattr(config, k))

    def service_configs(self, app: Flask) -> dict:
        """Customize service configs."""
        return {
            "record": Marc21CatalogueServiceConfig.build(app),
            "file": Marc21RecordFilesServiceConfig.build(app),
            "file_draft": Marc21DraftFilesServiceConfig.build(app),
        }

    def init_services(self, app: Flask) -> None:
        """Initialize services."""
        service_config = self.service_configs(app)

        self.records_service = Marc21CatalogueService(
            config=service_config["record"],
            files_service=FileService(service_config["file"]),
            draft_files_service=FileService(service_config["file_draft"]),
            pids_service=PIDsService(service_config["record"], PIDManager),
        )

        self.files_service = FileService(service_config["file"])

        self.draft_files_service = FileService(service_config["file_draft"])

        self.tasks_service = Marc21CatalogueTasksService(
            config=Marc21CatalogueTasksServiceConfig,
        )

    def init_resources(self) -> None:
        """Initialize resources."""
        self.record_resource = Marc21CatalogueRecordResource(
            service=self.records_service,
            config=Marc21CatalogueRecordResourceConfig,
        )
        self.record_catalgoue = Marc21CatalogueResource(
            service=self.records_service,
            config=Marc21CatalogueResourceConfig,
        )
        self.alma_proxy = Marc21CatalogueAlmaProxyResource(
            service=self.records_service,
            config=Marc21CatalogueAlmaProxyResourceConfig,
        )
        self.tasks_resource = Marc21CatalogueTasksResource(
            service=self.tasks_service,
            config=Marc21CatalogueTasksConfig,
        )


def finalize_app(app: Flask) -> None:
    """Finalize app."""
    init(app)


def api_finalize_app(app: Flask) -> None:
    """Finalize app for api."""
    init(app)


def init(app: Flask) -> None:
    """Init app."""
    # Register services - cannot be done in extension because
    # Invenio-Records-Resources might not have been initialized.

    ext = app.extensions["invenio-catalogue-marc21"]
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.records_service, service_id="marc21-catalogue-records")
    sregistry.register(ext.records_service.files, service_id="marc21-catalogue-files")
    sregistry.register(
        ext.records_service.draft_files,
        service_id="marc21-catalogue-draft-files",
    )

    # iregistry = app.extensions["invenio-indexer"].registry
    # iregistry.register(ext.records_service.indexer, indexer_id="marc21-records")
    # iregistry.register(
    #     ext.records_service.draft_indexer, indexer_id="marc21-records-drafts"
    # )
