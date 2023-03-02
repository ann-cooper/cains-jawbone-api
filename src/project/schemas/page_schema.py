from src.project.models import PageOrder
from src.project.services import mllw


class PageOrderSchema(mllw.SQLAlchemyAutoSchema):
    class Meta:
        model = PageOrder
        load_instance = True
