from flask import Blueprint

display_bp = Blueprint("display", __name__, template_folder="../templates/display")

from . import routes  # noqa: E402,F401


