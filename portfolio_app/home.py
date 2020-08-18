from flask import Blueprint, render_template

from portfolio_app.models import Post
import math


bp = Blueprint("home", __name__)


@bp.route("/")
def home_view():
    posts = Post.query.all()
    post_list = []
    for post in posts[:5]:
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

    n_article = len(posts) if len(posts) < 5 else 5

    reading_min = None

    return render_template(
        "/home/index.html",
        posts=post_list,
        n_article=n_article,
        reading_min=reading_min,
    )


@bp.route("/about")
def about_view():
    return render_template("/home/about.html")
