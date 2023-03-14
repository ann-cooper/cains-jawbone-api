from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class PageOrderForm(FlaskForm):
    page = IntegerField("Page", validators=[DataRequired()])
    order = IntegerField("Order")
    submit = SubmitField("Submit")
