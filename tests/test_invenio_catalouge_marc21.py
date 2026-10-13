# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT


"""Module tests."""

from flask import Flask

from invenio_catalogue_marc21 import InvenioCatalogueMarc21, __version__


def test_version() -> None:
    """Test version import."""
    assert __version__


def test_init() -> None:
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioCatalogueMarc21(app)
    assert "invenio-catalogue-marc21" in app.extensions

    app = Flask("testapp")
    ext = InvenioCatalogueMarc21()
    assert "invenio-catalogue-marc21" not in app.extensions
    ext.init_app(app)
    assert "invenio-catalogue-marc21" in app.extensions
