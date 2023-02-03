from src.project.models import ReferenceInfo

from src.project.services import mllw


class RefInfoSchema(mllw.SQLAlchemyAutoSchema):
    class Meta:

        model = ReferenceInfo
        load_instance = True

