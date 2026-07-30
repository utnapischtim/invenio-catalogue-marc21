# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""

from flask import current_app
from flask_principal import Identity
from invenio_records_marc21.services import Marc21RecordService
from invenio_records_resources.services.base import Service
from invenio_records_resources.services.records.results import RecordItem

from .tasks import import_task


class T:
    """Only for temprorary mocking."""

    def to_dict(self) -> dict:
        """To dict."""
        return {}


class Marc21CatalogueService(Marc21RecordService):
    """Marc21 record service class."""

    def add(self, identity: Identity, data: dict) -> RecordItem:
        """Add.

        this method does only creates a new record. this means that there is not
        yet added a entry to the children attribute in the parent node. this
        enables the option to clean up unused nodes by a task.

        the update draft method is then taking care of connecting the node to the parent.

        QUESTION:
        should the update_draft method be overritten or should that addition to
        parent functionality be done by a component

        QUESTION:
        should the add be safeguarded by a permission system?
        """
        return super().create(identity=identity, data=data)


class Marc21CatalogueTasksService(Service):
    """Marc21 catalogue progress service."""

    def progress(self, identity: Identity, pid: str) -> None:
        """Progress."""
        print(f"Marc21CatalogueTasksService.progress pid: {pid}, identity: {identity}")
        # use db directly, no indexing necessary
        # - get from table marc21_catalogue_tasks by pid, all lines
        # - return result

    def start(
        self,
        identity: Identity,  # noqa: ARG002
        pid: str,
        task: str,
        params: dict[str, str],
    ) -> T:
        """Start."""
        # TODO:
        # not every identity should be able to do every task

        match task:
            case "import":
                mapper_cls = current_app.config["MARC21_CATALOGUE_IMPORT_CLS_TYPES"][
                    # TODO: check why [0] is necessary, route definition wrong?
                    params["mapper_cls_type"][0]
                ]
                import_task.delay(pid, mapper_cls, params)
        # TODO:
        # check if there is a use case to return anything more useful as an empty dict
        return T()
