from flask import Flask

from home.views import home
from about.views import about
from projects.views import projects
from blog.views import blog
from admin.views import admin

app = Flask(__name__)
app.register_blueprint(home, url_prefix="")
app.register_blueprint(about, url_prefix="/about")
app.register_blueprint(projects, url_prefix="/projects")
app.register_blueprint(blog, url_prefix="/blog")
app.register_blueprint(admin, url_prefix="/admin")


if __name__ == "__main__":
    app.run(debug=True)
