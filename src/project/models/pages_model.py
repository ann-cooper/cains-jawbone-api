from src.project.services import db


class PageOrder(db.Model):
    __tablename__ = "page_order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page = db.Column(db.Integer, nullable=True)
    order = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, nullable=True)
