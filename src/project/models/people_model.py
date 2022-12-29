from src.project.services import pgdb


class People(pgdb.Model):
    """Characters mentioned and their role in the puzzle."""

    __tablename__ = "people"

    id = pgdb.Column(pgdb.Integer, primary_key=True, autoincrement=True)
    page = pgdb.Column(pgdb.Integer, nullable=True)
    name = pgdb.Column(pgdb.String, nullable=True)
    role = pgdb.Column(pgdb.String, nullable=True)
    created_date = pgdb.Column(pgdb.DateTime, nullable=True)
