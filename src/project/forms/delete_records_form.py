from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, validators


class DelRecordsForm(FlaskForm):
    name = StringField("Name", validators=[validators.optional()])
    page = IntegerField("Page", validators=[validators.optional()])
    id = IntegerField("ID", validators=[validators.DataRequired()])
    clue = StringField("Clue", validators=[validators.optional()])
    record_type = SelectField(
        "Type",
        choices=[
            ("people", "Character record"),
            ("pagerefs", "Page reference only"),
            ("pageorder", "Page order"),
            ("referenceinfo", "Reference info"),
        ],
        validators=[validators.DataRequired()],
    )
    submit = SubmitField("Delete")
