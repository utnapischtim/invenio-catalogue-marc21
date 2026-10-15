# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 catalogue fixture tasks."""

from copy import deepcopy
from pathlib import Path

from celery import shared_task
from flask_principal import Identity
from invenio_access.permissions import system_identity
from invenio_records_resources.services.files import FileService

from ..proxies import current_catalogue_marc21
from .demo import create_fake_file


def add_file_to_record(
    file_service: FileService,
    recid: str,
    file_path: Path,
    identity: Identity,
) -> None:
    """Add file to record."""
    filename = "Report.pdf"
    data = [{"key": filename}]

    with file_path.open(mode="rb") as file_pointer:
        file_service.init_files(id_=recid, identity=identity, data=data)
        file_service.set_file_content(
            id_=recid,
            file_key=filename,
            identity=identity,
            stream=file_pointer,
        )
        file_service.commit_file(id_=recid, file_key=filename, identity=identity)


@shared_task
def create_catalogue_marc21_record(
    data: dict,
    data_chapters: list,
    access: dict,
) -> None:
    """Create records for demo purposes."""
    identity = system_identity
    service = current_catalogue_marc21.records_service
    data_root = deepcopy(data)
    data_root["catalogue"] = {
        "root": "",
        "parent": "",
        "children": [],
    }
    draft_root = service.create(
        data=data_root,
        identity=identity,
        access=access,
    )
    # add fake file to record
    if data["files"]["enabled"]:
        file_path = create_fake_file()
        add_file_to_record(service.draft_files, draft_root.id, file_path, identity)

    # create chapters as draft to have the pid
    drafts = [draft_root]
    for chapter in data_chapters:
        c = deepcopy(chapter)
        c["catalogue"] = {
            "root": draft_root.id,
            "parent": draft_root.id,
            "children": [],
        }
        draft_chapter = service.create(
            data=c,
            identity=identity,
            access=access,
        )

        file_path = create_fake_file()
        add_file_to_record(service.draft_files, draft_chapter.id, file_path, identity)
        drafts.append(draft_chapter)

        for chapter_ in data_chapters:
            c = deepcopy(chapter_)
            c["catalogue"] = {
                "root": draft_root.id,
                "parent": draft_chapter.id,
                "children": [],
            }
            draft_chapter_ = service.create(
                data=c,
                identity=identity,
                access=access,
            )

            file_path = create_fake_file()
            add_file_to_record(
                service.draft_files,
                draft_chapter_.id,
                file_path,
                identity,
            )
            drafts.append(draft_chapter_)

    # publish drafts
    for draft in drafts:
        service.publish(id_=draft.id, identity=identity)
