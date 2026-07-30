# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 decorators backend."""

from collections.abc import Callable
from functools import wraps
from typing import TypedDict, Unpack

from flask import g
from invenio_records_resources.services.errors import PermissionDeniedError
from invenio_records_resources.services.files import FileService
from invenio_records_resources.services.files.results import FileList
from invenio_records_resources.services.records.results import RecordItem
from sqlalchemy.exc import NoResultFound

from ..proxies import current_catalogue_marc21
from ..services import Marc21CatalogueService


class KWARGS(TypedDict):
    """Typed dict for kwargs."""

    is_preview: bool
    pid_value: str
    files: FileList | None
    draft_files: FileList | None
    record: RecordItem


def _service() -> Marc21CatalogueService:
    """Get the record service."""
    return current_catalogue_marc21.records_service


def _files_service() -> FileService:
    """Get the record files service."""
    return current_catalogue_marc21.records_service.files


def _draft_files_service() -> FileService:
    """Get the record files service."""
    return current_catalogue_marc21.records_service.draft_files


def pass_draft[T](func: Callable[..., T]) -> Callable:
    """Decorate to retrieve the draft using the record service."""

    @wraps(func)
    def view(**kwargs: dict) -> T:
        """Wrap."""
        pid_value = kwargs.get("pid_value")

        # i am not sure if doing an edit before is the correct way, but with
        # this the draft will exist for sure and the schema will also exist
        _service().edit(id_=pid_value, identity=g.identity)
        kwargs["draft"] = _service().read_draft(id_=pid_value, identity=g.identity)
        return func(**kwargs)

    return view


def pass_draft_files[T](func: Callable[..., T]) -> Callable:
    """Decorate a view to pass a draft's files using the files service."""

    @wraps(func)
    def view(**kwargs: Unpack[KWARGS]) -> T:
        try:
            pid_value = kwargs.get("pid_value")
            files = _draft_files_service().list_files(
                id_=pid_value,
                identity=g.identity,
            )
            kwargs["draft_files"] = files

        except PermissionDeniedError:
            # this is handled here because we don't want a 404 on the landing
            # page when a user is allowed to read the metadata but not the
            # files
            kwargs["draft_files"] = None

        return func(**kwargs)

    return view


def pass_record_or_draft[T](f: Callable[..., T]) -> Callable:
    """Decorate to retrieve the record or draft using the record service."""

    @wraps(f)
    def view(**kwargs: Unpack[KWARGS]) -> T:
        pid_value = kwargs.get("pid_value")
        is_preview = kwargs.get("is_preview")

        if is_preview:
            try:
                record = _service().read_draft(id_=pid_value, identity=g.identity)
            except NoResultFound:
                try:
                    record = _service().read(id_=pid_value, identity=g.identity)
                except NoResultFound:
                    record = _service().edit(id_=pid_value, identity=g.identity)
        else:
            record = _service().read(id_=pid_value, identity=g.identity)

        kwargs["record"] = record
        return f(**kwargs)

    return view


def pass_record_files[T](f: Callable[..., T]) -> Callable:
    """Decorate a view to pass a record's files using the files service."""

    @wraps(f)
    def view(**kwargs: Unpack[KWARGS]) -> T:
        is_preview = kwargs.get("is_preview")
        pid_value = kwargs.get("pid_value")

        try:
            if is_preview:
                files = _draft_files_service().list_files(
                    id_=pid_value,
                    identity=g.identit,
                )
            else:
                files = _files_service().list_files(id_=pid_value, identity=g.identity)
        except PermissionDeniedError:
            files = None
        except NoResultFound:
            files = _files_service().list_files(id_=pid_value, identity=g.identity)

        kwargs["files"] = files

        return f(**kwargs)

    return view
