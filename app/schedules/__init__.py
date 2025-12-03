from flask import Blueprint

schedules_bp = Blueprint("schedules", __name__, template_folder="../templates/schedules")

from . import routes  # noqa: E402,F401


