from src.project.services import db


class People(db.Model):
    """Characters mentioned and their role in the puzzle."""

    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=True) # TODO must be unique
    role = db.Column(db.String, nullable=True)


class PageRefs(db.Model):
    """Pages on which characters are mentioned."""

    __tablename__ = "page_refs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page = db.Column(db.Integer, nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    name = db.Column(db.String, nullable=True)
