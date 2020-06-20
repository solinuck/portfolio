from flask import Blueprint, render_template


blog = Blueprint("blog", __name__, static_folder="static", template_folder="templates")


@blog.route("/")
def blog_view():
    return render_template("blog.html")
