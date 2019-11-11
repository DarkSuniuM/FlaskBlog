from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
