from flask import Blueprint, render_template

from .db import get_db


bp = Blueprint("home", __name__)


@bp.route("/")
def home_view():
    return render_template("/home/index.html")
