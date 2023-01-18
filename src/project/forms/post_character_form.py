from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from datetime import datetime


class CharacterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    page = IntegerField("Page", validators=[])
    role = StringField("Role", validators=[])
    submit = SubmitField("Submit")
