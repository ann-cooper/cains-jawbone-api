from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PageRefForm(FlaskForm):
    page = IntegerField("Page", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")
