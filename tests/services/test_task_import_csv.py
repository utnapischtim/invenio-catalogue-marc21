# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT


"""Test import csv."""

from csv import DictReader
from json import load
from pathlib import Path

from invenio_records_marc21.services.record.metadata import Marc21Metadata

from invenio_catalogue_marc21.services.tasks import build_data_from_csv_row


class ConvertTest:
    """Test class for converting."""

    def __init__(self, record: Marc21Metadata) -> None:
        """Construct."""

    def convert(self, row: dict, record: Marc21Metadata) -> None:
        """Convert."""
        for key, value in row.items():
            self.visit_column(key, value, record)

    def visit_column(self, key: str, value: str, record: Marc21Metadata) -> None:
        """Run column function."""

        def func_not_found(_: str, __: Marc21Metadata) -> None:
            msg = f"NO visitor node: '{key}'"
            raise ValueError(msg)

        visit_func = getattr(self, f"visit_{key}", func_not_found)
        visit_func(value, record)

    def visit_id(self, value: str, record: Marc21Metadata) -> None:
        """Visit ."""
        # add to 500 field

    def visit_doi(self, value: str, record: Marc21Metadata) -> None:
        """Visit DOI."""
        record.add_datafield("024.7..", subfs={"2": "doi", "a": value})
        record.add_datafield(
            "845.4.0.",
            subfs={"3": "Volltext", "u": f"https://doi.org/{value}", "z": "kostenfrei"},
        )

    def visit_filename(self, value: str, _: Marc21Metadata) -> None:
        """Visit filename."""
        self.filename = value

    def visit_title(self, value: str, record: Marc21Metadata) -> None:
        """Visit title."""
        record.emplace_datafield("245.1.0.", subfs={"a": value})

    def visit_year(self, value: str, record: Marc21Metadata) -> None:
        """Visit year."""
        # i think it goes into 245

    def visit_authors(self, value: str, record: Marc21Metadata) -> None:
        """Visit authors."""
        for author in value.split(";"):
            # todo extract affiliation and orcid from author
            record.add_datafield("700.1..", subfs={"a": author})


def test_import_from_csv() -> None:
    """Test import from csv."""
    parent = Path(__file__).parent

    with Path(f"{parent}/data/import.csv").open("r") as fp:
        reader = DictReader(fp)

        row = next(reader)  # consider only first
        data, filename = build_data_from_csv_row(row, mapper_cls=ConvertTest)

        with Path(f"{parent}/data/expected.json").open("r") as fp_expected:
            expected = load(fp_expected)
            assert data.json == expected
            assert filename == "lorem_ipsum_001.pdf"
