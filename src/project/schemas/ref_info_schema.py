from src.project.services import mllw
from marshmallow import fields


class RefInfoSchema(mllw.Schema):
    page = fields.Str()
    created_date = fields.Date()
    clue = fields.Str()
    reference = fields.Dict()