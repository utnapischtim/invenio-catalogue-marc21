# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Records error handlers."""

from flask import current_app, render_template
from flask_login import current_user


#
# Error handlers
#
def not_found_error(*_: tuple, **__: dict) -> tuple[str, int]:
    """Handle 'Not Found' errors."""
    return render_template(current_app.config["THEME_404_TEMPLATE"]), 404


def record_tombstone_error(*_: tuple, **__: dict) -> tuple[str, int]:
    """Tombstone page."""
    return render_template("invenio_records_marc21/tombstone.html"), 410


def record_permission_denied_error(*_: tuple, **__: dict) -> tuple[str, int]:
    """Handle permission denier error on record views."""
    if not current_user.is_authenticated:
        # trigger the flask-login unauthorized handler
        return current_app.login_manager.unauthorized()  # type: ignore[attr-defined,no-any-return]
    return render_template(current_app.config["THEME_403_TEMPLATE"]), 403
