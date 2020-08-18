from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login_view"

from portfolio_app import auth, blog, home, projects


# db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(home.bp)
app.register_blueprint(projects.bp)
app.add_url_rule("/", endpoint="index")
