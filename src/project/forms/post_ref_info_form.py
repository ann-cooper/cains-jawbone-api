from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RefInfoForm(FlaskForm):
    page = IntegerField("Page", validators=[DataRequired()])
    clue = StringField("Clue", validators=[DataRequired()])
    link = StringField("Reference link")
    info = TextAreaField("Reference info")
    submit = SubmitField("Submit")
