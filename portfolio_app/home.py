from flask import Blueprint, render_template

from .db import get_db
import math


bp = Blueprint("home", __name__)


@bp.route("/")
def home_view():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, imagename, intro, body, tags, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    posts = [dict(post) for post in posts]
    for post in posts:
        post["tags"] = eval(post["tags"])
        post["body"] = eval(post["body"])
    n_article = len(posts) if len(posts) < 5 else 5

    n_words = (
        post["intro"].count(" ") + post["body"].count(" ") + 4
    )  # 2 additional words at beggining and end.

    reading_min = int(math.ceil(n_words / 225))  # average wpm 225

    return render_template(
        "/home/index.html",
        posts=posts,
        n_article=n_article,
        reading_min=reading_min,
    )


@bp.route("/about")
def about_view():
    return render_template("/home/about.html")
