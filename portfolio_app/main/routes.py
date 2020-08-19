from flask import Blueprint, render_template
from portfolio_app.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home/")
def home_view():
    posts = Post.query.all()
    tags = []
    body = []
    posts = posts[:5]
    for post in posts:
        tags.append(eval(post.tags))
        body.append(eval(post.body))

    return render_template(
        "/main/index.html", posts=posts, tags=tags, body=body
    )


@main.route("/about/")
def about_view():
    return render_template("/main/about.html")


@main.route("/projects/")
def projects_view():
    return render_template("/main/projects.html")
