from src.project.models import PageRefs, People
from src.project.services import mllw


class PeopleSchema(mllw.SQLAlchemyAutoSchema):
    class Meta:

        model = People
        load_instance = True


class PageRefSchema(mllw.SQLAlchemyAutoSchema):
    class Meta:

        model = PageRefs
        load_instance = True
