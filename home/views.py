from flask import Blueprint, render_template
import os

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")


images_path = os.path.join("static", "images")


@home.route("/")
def home_view():
    return render_template("home.html", images_path=images_path)
