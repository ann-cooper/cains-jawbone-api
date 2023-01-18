from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField, validators




class DelRecordsForm(FlaskForm):
    name = StringField("Name", validators=[validators.optional()])
    page = IntegerField("Page", validators=[validators.optional()])
    id = IntegerField("ID", validators=[validators.optional()])
    record_type = SelectField("Type", choices=[("people", "Character record"), ("page_ref", "Page reference only"), ("page_order", "Page order"), ("ref_info", "Reference info")])
    submit = SubmitField("Delete")
