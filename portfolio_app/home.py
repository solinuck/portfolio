from flask import Blueprint, render_template, current_app
from github import Github
import base64

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
        post["created"] = post["created"].strftime("%m/%d/%Y, %H:%M:%S")
        post["created"] = post["created"][:7] + post["created"][9:10]
    n_article = len(posts) if len(posts) < 5 else 5

    n_words = (
        post["intro"].count(" ") + post["body"].count(" ") + 4
    )  # 2 additional words at beggining and end.

    reading_min = int(math.ceil(n_words / 225))  # average wpm 225

    username = "solinuck"
    # url = "https://api.github.com/users/{}".format(username)

    g = Github("17ed2ae3393526cd47ac67aeccb683d69c01ff31")

    user = g.get_user(username)

    repos = user.get_repos()
    project_img = []
    i = 1
    for repo in repos[:4]:
        try:
            project_img.append(
                repo.get_contents("/img/readme-example.png").download_url
            )
        except:
            project_img.append(
                f"{current_app.config['IMAGES_PATH']}/projects/project-{i}.jpeg"
            )
            i += 1
    return render_template(
        "/home/index.html",
        posts=posts,
        n_article=n_article,
        reading_min=reading_min,
        repos=repos,
        project_img=project_img,
    )


@bp.route("/about")
def about_view():
    return render_template("/home/about.html")
