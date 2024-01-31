from flask.views import MethodView

from src import logger
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import find_model

logger = logger.get_logger(__name__)


class Fields(MethodView):

    def get(self, model_selection: str):

        model, schema = find_model(key=model_selection)
        fields_dict = DataToModelMapper(models=[model]).extract_db_fields().keys_dict

        if len(fields_dict) > 1:
            return {
                "results": None,
                "status": 400,
                "message": "Too many models requested.",
            }
        elif len(fields_dict) < 1:
            return {
                "results": None,
                "status": 400,
                "message": "Select a model to return fields.",
            }

        match fields_dict:
            case {"People": x, **kw}:
                fields = fields_dict.get("People")
            case {"PageRefs": x, **kw}:
                fields = fields_dict.get("PageRefs")
            case {"PageOrder": x, **kw}:
                fields = fields_dict.get("PageOrder")
            case {"ReferenceInfo": x, **kw}:
                fields = fields_dict.get("ReferenceInfo")
            case _:
                fields = None

        return {"results": fields, "status": 200}
