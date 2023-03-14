from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import AnyOf, DataRequired


class CharacterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    page = IntegerField("Page", validators=[])
    role = StringField(
        "Role",
        validators=[
            AnyOf(
                values=["Murderer", "Victim", "Unknown", "Test"],
                message="Role must be one of: Murderer, Victim, Unknown, Test",
            )
        ],
    )
    submit = SubmitField("Submit")
