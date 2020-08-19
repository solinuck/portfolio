from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


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
    submit = SubmitField("Publish")
