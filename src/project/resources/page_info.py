from flask import request
from flask.views import MethodView

from src import logger
from src.project.models import PageRefs, People
from src.project.schemas import PageRefSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_next_id,
    get_record_by_id,
    get_record_by_name,
    get_record_by_page_name,
)

logger = logger.get_logger(__name__)


class PageInfoHandler(MethodView):
    def __init__(self):
        self.model = PageRefs
        self.schema = PageRefSchema()

    def get(self, page_id: int = None) -> dict:
        if page_id:
            results = get_record_by_id(model=PageRefs, id=page_id)
            results = self.schema.dump(results) if results else None
        else:
            results = dump_recent_records(model=self.model, schema=self.schema)

        results = results if results else {"message": "No records"}

        return {"results": results, "status": 200}

    def post(self, page_id: int = None) -> dict:
        """Add or update a page-info record

        Request body:
            {"page": int, "name": "str"}

        Returns:
            dict: id of updated record
        """
        records_to_add = []
        data = request.get_json()
        if data:
            new_id = get_next_id(model=self.model)
            data_objs = (
                DataToModelMapper(models=[self.model])
                .extract_db_fields()
                .data_unpack(data=data)
            )
            new_page_ref = DataToModelMapper.pg_data_load(
                model=self.model, data=data_objs.get("PageRefs")
            )
            check = get_record_by_page_name(
                model=self.model, page=new_page_ref.page, name=new_page_ref.name
            )
            if check:
                message = (
                    f"Not updating {check.page}, {check.name} because record exists."
                )
                logger.info(message)
                results = {"results": None}
            else:
                new_page_ref.id = new_id
                records_to_add.append(new_page_ref)
                character_check = get_record_by_name(
                    model=People, name=new_page_ref.name
                )
                message = f"New record created for {new_page_ref.page}"
                if character_check:
                    results = {
                        "results": {
                            "people": character_check.id,
                            "page_info": new_page_ref.id,
                        }
                    }
                else:  # character_check False
                    # Create new character record
                    new_character_id = get_next_id(model=People)
                    new_character = People(name=new_page_ref.name, id=new_character_id)
                    records_to_add.append(new_character)
                    message = (
                        message
                        + f" and new character record created for {new_character.name}."
                    )
                    results = {
                        "results": {
                            "people": new_character_id,
                            "page_info": new_page_ref.id,
                        }
                    }
            logger.info(message)
            db.session.add_all(records_to_add)
            db.session.commit()
            results["status"] = 200
            return results

    def put(self, page_id: int):
        # TODO edit button calls
        pass

    def delete(self, page_id: int) -> dict:
        """Delete page-info record.

        Args:
            page_id (int): id of page info record to delete

        Returns:
            dict: record id deleted
        """
        records_to_del = []
        record_check = get_record_by_id(model=self.model, id=page_id)

        if record_check:
            message = f"Deleting page info record id: {page_id}"
            records_to_del.append(record_check)
            results = {"results": record_check.id}
        else:
            message = f"No record found for id {page_id}."
            results = {"results": None}

        logger.info(message)
        [db.session.delete(rec) for rec in records_to_del if records_to_del]
        db.session.commit()
        results["status"] = 200

        return results
