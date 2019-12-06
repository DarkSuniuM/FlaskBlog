from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired


class FileUploadForm(FlaskForm):
    file = FileField(validators=[DataRequired()])