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

    def post(self, character_id: int = None):
        records_to_add = []
        data = request.get_json()
        character_id = character_id if character_id else get_next_id(model=People)
        if data:
            data_objs = (
                DataToModelMapper(models=[PageRefs, People])
                .extract_db_fields()
                .data_unpack(data=data)
            )
            character_record = DataToModelMapper.pg_data_load(
                model=People, data=data_objs.get("People")
            )
            page_ref = DataToModelMapper.pg_data_load(
                model=PageRefs, data=data_objs.get("PageRefs")
            )

            # Check for existing record
            character_check = get_record_by_id(model=People, id=character_record.id)

            if character_check:
                character_check.role = character_record.role
                character_check.name = character_record.name
                records_to_add.append(character_check)
                page_ref.people_id = character_check.id
                pages_check = search_records(
                    model=PageRefs,
                    filters=[
                        (PageRefs.people_id == character_check.id),
                    ],
                )

                if pages_check:
                    # Update character name in any existing page records.
                    logger.info(
                        f"Found {len(pages_check)} records for people_id {character_record.id}."
                    )
                    message = f"Updating record for {character_check.name}."
                    # Update character name in page records
                    updated_page_refs = []
                    for record in pages_check:
                        if record.name != character_check.name:
                            record.name = character_check.name
                        updated_page_refs.append(record)
                    records_to_add.extend(updated_page_refs)

                    results = {
                        "results": {
                            "character": self.schema.dump(character_check),
                            "page": [record.id for record in updated_page_refs],
                        },
                        "status": 200,
                    }

                # Pages check returned 0 records
                else:
                    if page_ref:
                        page_id = get_next_id(model=PageRefs)
                        page_ref.id = page_id
                        records_to_add.append(page_ref)
                        message = f"Updating record for {character_check.name} and creating page_ref {page_ref.id}."
                        results = {
                            "results": {
                                "character": self.schema.dump(character_check),
                                "page": page_ref.id,
                            },
                            "status": 200,
                        }
                logger.info(message)

            # Record not found for character id
            else:
                logger.info("Creating new character and page ref records.")
                if character_record:
                    character_record.id = character_id
                    records_to_add.append(character_record)
                    page_ref.people_id = character_record.id
                    records_to_add.append(page_ref)
                    results = {
                        "results": {
                            "character": character_record.id,
                            "page": page_ref.id,
                        },
                        "status": 200,
                    }

            db.session.add_all(records_to_add)
            db.session.commit()
            return results

    def put(self, character_id: int):
        # TODO for edits
        pass

    def delete(self, character_id: int):
        """Delete a character record.

        Args:
            character_id (int): url param

        Request body:
            {"name": "name to delete"}

        Returns:
            dict: records deleted
        """
        records_to_del = []
        logger.info(f"Delete request: {request}")
        record_check = get_record_by_id(model=self.model, id=character_id)

        if record_check:
            message = f"Deleting records for {record_check.id}"
            records_to_del.append(record_check)
            page_refs = get_all_records(
                model=PageRefs, filters=[(PageRefs.name == record_check.name)]
            )
            if page_refs:
                records_to_del.extend(page_refs)
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
