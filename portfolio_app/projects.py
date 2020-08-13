from flask import Blueprint, render_template


bp = Blueprint("projects", __name__, url_prefix="/projects")


@bp.route("/")
def projectlist_view():
    return render_template("projects/projectlist.html")


@bp.route("/<name>")
def single_project(name):
    return render_template("projects/single_project.html")
