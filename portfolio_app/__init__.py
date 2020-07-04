import os

from flask import Flask
from . import db
from . import auth
from . import blog
from . import home


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.DevelopmentConfig")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    return app
