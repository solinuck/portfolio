import os
import re
import secrets
import math
from datetime import datetime

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
    abort,
)

from flask_login import login_required, current_user
from portfolio_app.forms import PostForm
from portfolio_app.models import Post
from portfolio_app import db


today = datetime.today()
if len(str(today.month)) == 1:
    today_month = "0" + str(today.month)
else:
    today_month = str(today.month)


today_year = str(today.year)[2:]

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
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "Oktober",
        "11": "November",
        "12": "December",
    }

    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_dict = {}
        post_dict["id"] = post.id
        post_dict["title"] = post.title
        post_dict["intro"] = post.intro
        post_dict["image_file"] = post.image_file
        post_dict["tags"] = eval(post.tags)
        post_dict["date_posted"] = post.date_posted.strftime(
            "%m/%d/%Y, %H:%M:%S"
        )
        post_dict["date_posted"] = (
            post_dict["date_posted"][:7] + post_dict["date_posted"][9:10]
        )
        post_dict["body"] = eval(post.body)
        n_words = (
            post.intro.count(" ") + post.body.count(" ") + 4
        )  # 2 additional words at beggining and end.
        post_dict["reading_min"] = int(
            math.ceil(n_words / 225)
        )  # average wpm 225
        post_list.append(post_dict)

    if search is not None:
        if request.method == "POST":
            search = request.form["search"]
        if search.replace(" ", "") != "":
            search_posts = search_func(post_list, search)
    else:
        search_posts = post_list

    return render_template(
        "blog/bloglist.html",
        posts=post_list,
        search_posts=search_posts,
        search=search,
        months=months,
        year=year,
        month=month,
        expandsearch=expandsearch,
    )


def search_func(post_list, search):
    search_words = re.sub("[^A-Za-z0-9 ]+", "", search.lower())
    search_words = search_words.split()
    ids = []
    for post in post_list:
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

    return [post for post in post_list if post["id"] in ids]


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.config["BLOG_UPLOADS"], picture_fn
    )
    form_image.save(picture_path)
    return picture_fn


@bp.route("/<title>-<int:id>/")
def single_article_view(id, title):
    curr_post = Post.query.get_or_404(id)
    curr_post = post_in_dict(curr_post)

    prev_post = Post.query.get(id - 1)
    if prev_post:
        prev_post = post_in_dict(curr_post)

    next_post = Post.query.get(id + 1)
    if next_post:
        next_post = post_in_dict(curr_post)
    return render_template(
        "blog/article.html",
        post=curr_post,
        prev_post=prev_post,
        next_post=next_post,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_view():
    form = PostForm()
    if form.validate_on_submit():
        image_file = save_image(form.image.data)
        tags = [
            request.form[f"tag{n}"]
            for n in range(5)
            if f"tag{n}" in request.form
        ]
        html_body = str(form.body.data.replace("\r", "").split("\n"))

        post = Post(
            title=form.title.data,
            author=current_user,
            intro=form.intro.data,
            image_file=image_file,
            body=html_body,
            tags=repr(tags),
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("blog.bloglist_view"))

    return render_template(
        "blog/create_article.html", legend="New Post", form=form
    )


@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_view(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            post.image_file = image_file

        post.title = form.title.data
        post.intro = form.intro.data
        post.body = str(form.body.data.replace("\r", "").split("\n"))
        post.tags = repr(
            [
                request.form[f"tag{n}"]
                for n in range(5)
                if f"tag{n}" in request.form
            ]
        )
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for("blog.bloglist_view"))

    post = post_in_dict(post)
    form.title.data = post["title"]
    form.intro.data = post["intro"]
    body_string = ""
    for i, p in enumerate(post["body"]):
        if p == "":
            p = "\n"
        body_string += p
    form.body.data = body_string
    form.image.data = post["image_file"]

    form.tag0.data = post["tags"][0]

    return render_template(
        "blog/create_article.html",
        legend="Update Post",
        form=form,
        tags=post["tags"],
        image_file=True,
    )


@bp.route("<int:id>/delete")
@login_required
def delete_view(id):
    post = Post.query.get_or_404(id)
    os.remove(
        os.path.join(current_app.config["BLOG_UPLOADS"], post["imagename"])
    )
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.bloglist_view"))


def post_in_dict(posts):
    post_dict = {}
    post_dict["id"] = posts.id
    post_dict["title"] = posts.title
    post_dict["intro"] = posts.intro
    post_dict["image_file"] = posts.image_file
    post_dict["tags"] = eval(posts.tags)
    post_dict["date_posted"] = posts.date_posted.strftime(
        "%m/%d/%Y, %H:%M:%S"
    )
    post_dict["date_posted"] = (
        post_dict["date_posted"][:7] + post_dict["date_posted"][9:10]
    )
    post_dict["body"] = eval(posts.body)
    n_words = (
        posts.intro.count(" ") + posts.body.count(" ") + 4
    )  # 2 additional words at beggining and end.
    post_dict["reading_min"] = int(
        math.ceil(n_words / 225)
    )  # average wpm 225
    return post_dict
