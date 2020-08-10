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

bp = Blueprint("projects", __name__, url_prefix="/projects")


@bp.route("/")
def projectlist_view():
    return render_template("projects/projectlist.html")
