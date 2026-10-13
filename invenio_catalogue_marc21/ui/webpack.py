# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {
                "invenio-catalogue-marc21-theme": "./less/invenio_catalogue_marc21/theme.less",
                "invenio-catalogue-marc21-deposit": "./js/invenio_catalogue_marc21/deposit/index.js",
                # "invenio-catalogue-marc21-landing-page": "./js/invenio_catalogue_marc21/landing_page/index.js",
            },
            "dependencies": {
                "@babel/runtime": "^7.9.0",
                "d3-hierarchy": "^1.1.9",
                "d3-shape": "^1.3.7",
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                "react-i18next": "^11.11.0",
            },
            "aliases": {
                "@js/invenio_catalogue_marc21": "js/invenio_catalogue_marc21",
                "@less/invenio_catalogue_marc21": "./less/invenio_catalogue_marc21",
                "@translations/invenio_catalogue_marc21": "translations/invenio_catalogue_marc21",
            },
        },
    },
)
