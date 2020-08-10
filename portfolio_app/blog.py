import os

import re
import math
from datetime import datetime

today = datetime.today()
if len(str(today.month)) == 1:
    today_month = "0" + str(today.month)
else:
    today_month = str(today.month)


today_year = str(today.year)[2:]
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    g,
    redirect,
    url_for,
    abort,
    current_app,
)
from werkzeug.utils import secure_filename

from .auth import login_required
from .db import get_db

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route(
    "/",
    defaults={
        "search": None,
        "year": today_year,
        "month": today_month,
        "expandsearch": False,
    },
    methods=("GET", "POST"),
)
@bp.route(
    "/<year>/<month>/expand<expandsearch>",
    defaults={"search": None},
    methods=("GET", "POST"),
)
@bp.route(
    "/<year>/<month>/expand<expandsearch>/<search>",
    methods=("GET", "POST"),
)
@bp.route(
    "/<search>",
    defaults={
        "year": today_year,
        "month": today_month,
        "expandsearch": False,
    },
    methods=("GET", "POST"),
)
def bloglist_view(search, expandsearch, year, month):
    months = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "Oktober": "10",
        "November": "11",
        "December": "12",
    }

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

    n_words = (
        post["intro"].count(" ") + post["body"].count(" ") + 4
    )  # 2 additional words at beggining and end.

    reading_min = int(math.ceil(n_words / 225))  # average wpm 225

    if search is not None:
        if request.method == "POST":
            search = request.form["search"]
        if search.replace(" ", "") != "":
            search_posts = search_func(posts, search)
    else:
        search_posts = posts

    return render_template(
        "blog/bloglist.html",
        posts=posts,
        search_posts=search_posts,
        search=search,
        reading_min=reading_min,
        months=months,
        year=year,
        month=month,
        expandsearch=expandsearch,
    )


def search_func(posts, search):
    search_words = re.sub("[^A-Za-z0-9 ]+", "", search.lower())
    search_words = search_words.split()
    ids = []
    for post in posts:
        title = post["title"]
        tags = [
            tag_word
            for tag in post["tags"]
            for tag_word in tag.lower().split()
        ]
        title_words = title.lower().replace("-", " ").split()
        all_words = title_words + tags

        for search_word in search_words:
            if search_word in all_words:
                ids.append(post["id"])

    return [post for post in posts if post["id"] in ids]


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create_view():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        intro = request.form["intro"]
        image = request.files["image"]
        imagename = None
        tags = [
            request.form[f"tag-{n}"]
            for n in range(5)
            if f"tag-{n}" in request.form
        ]

        error = None

        if request.files["image"] and "filesize" in request.cookies:
            if not allowed_image_filesize(request.cookies["filesize"]):
                error = "Filesize exceeded maximum limit."

            if image.filename == "":
                error = "no filename"

            if allowed_image(image.filename):
                imagename = secure_filename(image.filename)
                n = 0
                while os.path.isfile(
                    os.path.join(
                        current_app.config["IMAGE_UPLOADS"], imagename
                    )
                ):
                    len_suff = len(image.filename.split(".")[1]) + 1
                    imagename = (
                        imagename[:-len_suff]
                        + f"{n}"
                        + imagename[-len_suff:]
                    )
                    n += 1

                image.save(
                    os.path.join(
                        current_app.config["IMAGE_UPLOADS"], imagename
                    )
                )
            else:
                error = "That file extension is not allowed."

        if not title:
            error = "Title is required."

        if len(tags) == 0:
            error = "One tag is required."

        if error is not None:
            flash(error)
            redirect(request.url)
        else:
            html_body = str(body.replace("\r", "").split("\n"))

            db = get_db()
            db.execute(
                "INSERT INTO post (title, imagename, intro, body, tags, author_id)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (
                    title,
                    imagename,
                    intro,
                    html_body,
                    repr(tags),
                    g.user["id"],
                ),
            )
            db.commit()
            return redirect(url_for("blog.bloglist_view"))

    return render_template("blog/create_article.html")


def get_post(id, check_author=True, check_other=False):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, imagename, intro, body, tags, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        if not check_other:
            abort(404, "Article id {0} doesn't exist.".format(id))
    else:
        post = dict(post)
        post["tags"] = eval(post["tags"])
        post["body"] = eval(post["body"])

    if check_author and post["author_id"] != g.user["id"]:
        if not check_other:
            abort(403)

    return post


@bp.route("/<title>-<int:id>/")
def single_article_view(id, title):
    curr_post = get_post(id, False)

    # try:
    prev_post = get_post(id - 1, check_author=False, check_other=True)
    next_post = get_post(id + 1, check_author=False, check_other=True)
    return render_template(
        "blog/article.html",
        post=curr_post,
        prev_post=prev_post,
        next_post=next_post,
    )


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update_view(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        intro = request.form["intro"]
        image = request.files["image"]
        imagename = "project-3.jpeg"
        tags = [
            request.form[f"tag-{n}"]
            for n in range(5)
            if f"tag-{n}" in request.form
        ]
        error = None

        if not title:
            error = "Title is required."

        if tags[0] == "":
            error = "One tag is required."

        if request.files["image"] and "filesize" in request.cookies:
            if not allowed_image_filesize(request.cookies["filesize"]):
                error = "Filesize exceeded maximum limit"

            if image.filename == "":
                error = "no filename"

            if allowed_image(image.filename):
                imagename = secure_filename(image.filename)

                image.save(
                    os.path.join(
                        current_app.config["IMAGE_UPLOADS"], imagename
                    )
                )
            else:
                error = "That file extension is not allowed"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, imagename = ?, intro = ?, body = ?, tags= ?"
                " WHERE id = ?",
                (title, imagename, intro, body, repr(tags), id),
            )
            db.commit()
            return redirect(url_for("blog.bloglist_view"))

    return render_template("blog/update.html", post=post)


@bp.route("<int:id>/delete")
@login_required
def delete_view(id):
    post = get_post(id)
    os.remove(
        os.path.join(
            current_app.config["IMAGE_UPLOADS"], post["imagename"]
        )
    )
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.bloglist_view"))


def allowed_image(filename):
    # We only want files with a . in the filename
    if "." not in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= current_app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False
