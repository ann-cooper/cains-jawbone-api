import datetime
from typing import Optional

from attrs import define, field

from src.project.services import db


@define
class _ReferenceInfo:
    page: int = field()
    clue: str = field()
    source: str = field()
    link: str = field()
    info: str = field()
    created_date: datetime.date = field(default=None)
    _id: Optional[str] = field(default=None)

    def __attrs_post_init__(self):
        if not self.created_date:
            self.created_date = datetime.date.today().isoformat()


class ReferenceInfo(db.Model):
    """Clue reference research info."""

    __tablename__ = "references"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page = db.Column(db.Integer, nullable=False)
    clue = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=True)
    info = db.Column(db.String, nullable=True)
