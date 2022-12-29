from flask import request
from flask.views import MethodView

from src import logger
from src.project.models.people_model import People
from src.project.services import pgdb
from src.project.utils.sqla_query_helper import (get_all_records,
                                                 get_record_by_id,
                                                 search_records)

logger = logger.get_logger(__name__)


class Hello(MethodView):
    def get(self):
        return ({"message": "Hello!"}, 200)


class Characters(MethodView):
    def get(self, character_id):
        if character_id is None:
            results = get_all_records(model=People)
            if results:
                return (results.items, 200)
            else:
                return ({"message": "No records."}, 400)
        else:
            results = get_record_by_id(model=People, id=character_id)
            if results:
                return (results, 200)
            else:
                return ({"message": f"{character_id} not found."}, 400)

    def post(self):
        character_data = request.get_json(force=True)
        new_character = People(**character_data)

        character_check = search_records(
            model=People, filters=(People.name == new_character.name)
        )
        if character_check:
            return ({"message": f"A record exists for {new_character.name}"}, 400)
        else:
            pgdb.session.add(new_character)
            pgdb.session.commit()

            return ({"message": f"Saving record for {new_character}"}, 200)
