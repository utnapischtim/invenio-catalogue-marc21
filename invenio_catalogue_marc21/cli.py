# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Command-line tools for demo module."""

from collections.abc import Callable
from functools import wraps

import click
from flask.cli import with_appcontext

from .fixtures.demo import create_fake_catalogue_record
from .fixtures.tasks import create_catalogue_marc21_record


def wrap_messages(before: str, after: str) -> Callable:
    """Wrap messages with entry and exit message."""

    def decorator[T](func: Callable[..., T]) -> Callable:
        @wraps(func)
        def wrapper(**kwargs: dict) -> None:
            """Wrap."""
            click.secho(before, fg="blue")
            try:
                func(**kwargs)
            except RuntimeError as error:
                click.secho(str(error), fg="red")
            else:
                click.secho(after, fg="green")

        return wrapper

    return decorator


@click.group()
def catalogue() -> None:
    """InvenioMarc21 records commands."""


@catalogue.command("demo")
@with_appcontext
@click.option(
    "--number",
    "-n",
    "n_records",
    default=1,
    show_default=True,
    type=int,
    help="Number of records will be created.",
)
@click.option(
    "--chapters",
    "-c",
    "n_chapters",
    default=15,
    show_default=True,
    type=int,
    help="Number of chapters will be created.",
)
@click.option(
    "--disable-files",
    default=False,
    is_flag=True,
    type=bool,
    help="disable file creation.",
)
@wrap_messages(
    before="Creating demo records...",
    after="Created records!",
)
def demo(
    n_records: int,
    n_chapters: int,
    *,
    disable_files: bool,
) -> None:
    """Create number of fake records for demo purposes."""
    for _ in range(n_records):
        data, data_chapters, data_access = create_fake_catalogue_record(
            n_chapters,
            files=not disable_files,
        )
        create_catalogue_marc21_record.delay(data, data_chapters, data_access)
