from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CharacterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    page = IntegerField("Page", validators=[])
    role = StringField("Role", validators=[])
    submit = SubmitField("Submit")
