from src.project.app import pgdb


class Pages(pgdb.Model):
    __tablename__ = "pages"

    id = pgdb.Column(pgdb.Integer, primary_key=True, autoincrement=True)
    page = pgdb.Column(pgdb.Integer, nullable=True)
    order = pgdb.Column(pgdb.String, nullable=True)
    created_date = pgdb.Column(pgdb.DateTime, nullable=True)
