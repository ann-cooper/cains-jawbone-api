from flask import flash, request
from flask.views import MethodView

from src import logger
from src.project.models import PageRefs, People
from src.project.schemas.people_schema import PeopleSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_all_records,
    get_next_id,
    get_record_by_id,
    get_record_by_name,
    search_records,
)

logger = logger.get_logger(__name__)


class Characters(MethodView):
    def __init__(self):
        self.model = People
        self.schema = PeopleSchema()

    def get(self, character_id: int = None):
        if character_id:
            results = get_record_by_id(model=self.model, id=character_id)
            results = self.schema.dump(results) if results else None
        else:
            results = dump_recent_records(model=self.model, schema=self.schema)
        
        results = results if results else {"message": "No records"}

        return {"results": results, "status": 200}

    def post(self):
        records_to_add = []
        data = request.get_json()
        if data:
            new_id = get_next_id(model=People)
            data_objs = (
                DataToModelMapper(models=[PageRefs, People], data=data)
                .extract_db_fields()
                .data_unpack()
                .new_objs
            )
            new_character = DataToModelMapper.pg_data_load(
                model=People, data=data_objs.get("People")
            )
            new_page_ref = DataToModelMapper.pg_data_load(
                model=PageRefs, data=data_objs.get("PageRefs")
            )
            # Check for existing record
            character_check = get_record_by_name(model=People, name=new_character.name)

            if character_check:
                character_check.role = new_character.role
                records_to_add.append(character_check)
                new_page_ref.people_id = character_check.id

                pages_check = search_records(
                    model=PageRefs,
                    filters=[
                        (PageRefs.page == new_page_ref.page),
                        (PageRefs.people_id == character_check.id),
                    ],
                )
                if len(pages_check) > 0:
                    logger.info(
                        f"A record for page {new_page_ref.page} for character name {character_check.name} and people_id {character_check.id} already exists."
                    )
                    message = f"Updating record for {character_check.name} but not page_ref {new_page_ref.page} because a record for {character_check.name} on page {new_page_ref.page} exists."
                    results = {
                        "results": {
                            "character": self.schema.dump(character_check),
                            "page": None,
                        },
                        "staus": 200,
                    }
                else:
                    records_to_add.append(new_page_ref)
                    message = f"Updating record for {character_check.name} and page_ref {new_page_ref.page}"
                    results = {
                        "results": {
                            "character": self.schema.dump(character_check),
                            "page": new_page_ref.page,
                        },
                        "status": 200,
                    }
                flash(message=message)

            else:
                flash("Creating new record")
                if new_character:
                    new_character.id = new_id
                    records_to_add.append(new_character)
                    new_page_ref.people_id = new_character.id
                    records_to_add.append(new_page_ref)
                    results = {
                        "results": {
                            "character": new_character.id,
                            "page": new_page_ref.id,
                        },
                        "status": 200,
                    }

            db.session.add_all(records_to_add)
            db.session.commit()
            return results

    def delete(self, character_id: int):
        """Delete a character record.

        Args:
            character_id (int): url param

        Request body:
            {"name": "name to delete"}

        Returns:
            dict: records delected
        """
        records_to_del = []
        data = request.get_json()
        record_check = get_record_by_id(
            model=self.model,
            id=character_id,
            filters=[(People.name == data.get("name"))],
        )

        if record_check:
            message = f"Deleting records for {record_check.id}"
            records_to_del.append(record_check)
            page_refs = get_all_records(
                model=PageRefs, filters=[(PageRefs.name == record_check.name)]
            )
            if page_refs:
                [records_to_del.append(rec) for rec in page_refs]
                message = (
                    message
                    + f"Deleting records for {record_check.name} and pages {[x.page for x in page_refs]}"
                )
                results = {
                    "results": {
                        "character": record_check.id,
                        "page": [x.page for x in page_refs],
                    },
                    "status": 200,
                }
            else:
                message = f"Record not found for {record_check.page}"
                results["results"]["page"] = None

            flash(message=message)

            [db.session.delete(rec) for rec in records_to_del if records_to_del]
            db.session.commit()
        else:
            results = {"results": None, "status": 200}
        return results
