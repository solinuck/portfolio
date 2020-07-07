import os
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


@bp.route("/")
def bloglist_view():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, imagename, intro, body, tags, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    tags = [eval(post["tags"]) for post in posts]
    return render_template("blog/bloglist.html", posts=posts, tags=tags)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create_view():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        intro = request.form["intro"]
        image = request.files["image"]
        imagename = "project-3.jpeg"
        tags = [request.form[f"tag-{n}"] for n in range(5) if f"tag-{n}" in request.form]

        error = None

        if request.files["image"] and "filesize" in request.cookies:
            if not allowed_image_filesize(request.cookies["filesize"]):
                error = "Filesize exceeded maximum limit."

            if image.filename == "":
                error = "no filename"

            if allowed_image(image.filename):
                imagename = secure_filename(image.filename)

                image.save(os.path.join(current_app.config["IMAGE_UPLOADS"], imagename))
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
            db = get_db()
            db.execute(
                "INSERT INTO post (title, imagename, intro, body, tags, author_id)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (title, imagename, intro, body, repr(tags), g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.bloglist_view"))

    return render_template("blog/create_article.html")


def get_post(id, check_author=True):
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
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<title>_<int:id>/")
def single_article_view(id, title):
    post = get_post(id, False)
    tags = eval(post["tags"])
    return render_template("blog/article.html", post=post, tags=tags)


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
        tags = [request.form[f"tag-{n}"] for n in range(5) if f"tag-{n}" in request.form]
        error = None

        if not title:
            error = "Title is required."

        if len(tags) == 0:
            error = "One tag is required."

        if request.files["image"] and "filesize" in request.cookies:
            if not allowed_image_filesize(request.cookies["filesize"]):
                error = "Filesize exceeded maximum limit"

            if image.filename == "":
                error = "no filename"

            if allowed_image(image.filename):
                imagename = secure_filename(image.filename)

                image.save(os.path.join(current_app.config["IMAGE_UPLOADS"], imagename))
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
    get_post(id)
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
