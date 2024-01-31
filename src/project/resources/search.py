from flask import request
from flask.views import MethodView

from src import logger
from src.project.utils.query_helper import find_model, search_records

logger = logger.get_logger(__name__)


class Search(MethodView):
    def get(self):
        return {"results": "placeholder", "status": 200}

    def post(self):
        """Return records for any model based on params in request data.

        Returns:
            dict: {"results": [dict], "status": int}
        """
        data = request.get_json()
        selected_record_type = data.pop("selected_name")

        model, schema = find_model(key=selected_record_type)
        schema = schema()

        # Build query filters
        filters = []
        for k, v in data.items():
            column = getattr(model, k, None)
            if column and v:
                filters.append((getattr(column, "__eq__")(v)))

        results = search_records(model=model, filters=filters)
        if results:
            results = [schema.dump(record) for record in results]

        return {"results": results, "status": 200}
