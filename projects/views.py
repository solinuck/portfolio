from flask import Blueprint, render_template

projects = Blueprint(
    "projects", __name__, static_folder="static", template_folder="templates"
)


@projects.route("/")
def projects_view():
    return render_template("projects.html")
