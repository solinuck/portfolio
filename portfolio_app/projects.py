from github import Github
from flask import Blueprint, render_template, current_app


bp = Blueprint("projects", __name__, url_prefix="/projects")


@bp.route("/")
def projectlist_view():
    username = "solinuck"

    g = Github(current_app.config["GITHUB_TOKEN"])

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
        "projects/projectlist.html", repos=repos, project_img=project_img
    )


@bp.route("/<name>")
def single_project(name):
    return render_template("projects/single_project.html")
