from marshmallow import fields

from src.project.services import mllw


class RefInfoSchema(mllw.Schema):
    page = fields.Str()
    created_date = fields.Date()
    clue = fields.Str()
    reference = fields.Dict()
