from src.project.app import db


class Pages(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page = db.Column(db.Integer, nullable=True)
    order = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, nullable=True)