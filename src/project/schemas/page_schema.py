from src.project.models.pages_model import PageOrder
from src.project.services import mllw


class PageOrderSchema(mllw.SQLAlchemyAutoSchema):
    class Meta:

        model = PageOrder
        load_instance = True