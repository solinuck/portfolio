from flask import Blueprint, render_template

from .db import get_db


bp = Blueprint("home", __name__)


@bp.route("/")
def home_view():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, intro, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("/home/index.html", posts=posts)


@bp.route("/about")
def about_view():
    return render_template("/home/about.html")
