from datetime import datetime
from portfolio_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    intro = db.Column(db.String(200), nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default.jpg"
    )
    body = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(75), nullable=False)
    # tag1 = db.Column(db.String(15))
    # tag2 = db.Column(db.String(15))
    # tag3 = db.Column(db.String(15))
    # tag4 = db.Column(db.String(15))
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.tags}')"
