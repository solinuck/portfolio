from github import Github
from flask import Blueprint, render_template


bp = Blueprint("projects", __name__, url_prefix="/projects")


@bp.route("/")
def projectlist_view():
    return render_template("projects/projectlist.html")


@bp.route("/<name>")
def single_project(name):
    username = "solinuck"
    url = "https://api.github.com/users/{}".format(username)

    g = Github()

    user = g.get_user(username)

    for repo in user.get_repos():
        readme = repo.get_readme().decoded_content
    return render_template(
        "projects/single_project.html", name=name, readme=readme, url=url
    )
