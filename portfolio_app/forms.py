from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from portfolio_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email is taken. Please choose a different one."
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=5)]
    )
    submit = SubmitField("Login")


class PostForm(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired(), Length(min=2, max=100)]
    )
    intro = TextAreaField(
        "Intro", validators=[DataRequired(), Length(min=2, max=200)]
    )
    image = FileField(
        "Select Image", validators=[FileAllowed(["jpg", "jpeg", "png"])]
    )
    body = TextAreaField("Body", validators=[DataRequired()])
    tag0 = StringField(
        "tag0", validators=[DataRequired(), Length(min=2, max=15)]
    )
    # tag1 = StringField(
    #     "tag1", validators=[Length(min=2, max=15)], default=""
    # )
    # tag2 = StringField(
    #     "tag2", validators=[Length(min=2, max=15)], default=""
    # )
    # tag3 = StringField(
    #     "tag3", validators=[Length(min=2, max=15)], default=""
    # )
    # tag4 = StringField(
    #     "tag4", validators=[Length(min=2, max=15)], default=""
    # )
    submit = SubmitField("Publish")
