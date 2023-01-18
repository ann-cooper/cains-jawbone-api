from src.project.models.people_model import People, PageRefs
from src.project.services import mllw


class PeopleSchema(mllw.SQLAlchemyAutoSchema):
    class Meta:

        model = People
        load_instance = True

class PageRefSchema(mllw.SQLAlchemyAutoSchema):
    class Meta:

        model = PageRefs
        load_instance = True