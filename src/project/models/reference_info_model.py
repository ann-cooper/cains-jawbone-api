from src.project.services import db
from src.project.models.mongo_validation import mongo_dict_field_validator

class ReferenceInfo(db.Document):
    """Clue reference research info."""

    _id = db.ObjectIdField(required=True)
    page = db.IntField(required=True)
    clue = db.StringField(required=True)
    reference = db.DictField(
        required=True, default={}, validation=mongo_dict_field_validator
    )
    created_date = db.ComplexDateTimeField(required=True)

    meta = {"collection": "references"}
