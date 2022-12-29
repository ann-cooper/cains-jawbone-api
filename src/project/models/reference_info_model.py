from src.project.services import mgdb


class ReferenceInfo(mgdb.Document):
    """Clue reference research info."""

    _id = mgdb.ObjectIdField(required=True)
    page = mgdb.IntField(required=True)
    clue = mgdb.StringField(required=True)
    reference = mgdb.DictField(required=True, default={})
    created_date = mgdb.ComplexDateTimeField(required=True)

    meta = {"collection": "references"}
