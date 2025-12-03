from flask import Blueprint

icons_bp = Blueprint("icons", __name__)

from . import routes

