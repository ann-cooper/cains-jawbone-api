from flask import flash, url_for, request
from flask.views import MethodView

from src import logger
from src.project.models import ReferenceInfo
from src.project.schemas import RefInfoSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_next_id,
    get_record_by_page_clue,
    get_record_by_id
)

logger = logger.get_logger(__name__)


class ReferenceInfoHandler(MethodView):
    def __init__(self):
        self.schema = RefInfoSchema()
        self.model = ReferenceInfo

    def get(self, ref_id: int = None) -> dict:
        if ref_id:
            results = get_record_by_id(model=self.model, id=ref_id)
            results = self.schema.dump(results) if results else None
        else:
            results = dump_recent_records(model=ReferenceInfo, schema=self.schema)
        
        results = results if results else {"message": "No records", "status": 200}

        return results

    def post(self) -> dict:
        records_to_add = []
        data = request.get_json()
        if data:
            new_id = get_next_id(model=ReferenceInfo)
            data_objs = (
                DataToModelMapper(models=[ReferenceInfo], data=data)
                .extract_db_fields()
                .data_unpack()
                .new_objs
            )
            new_reference = DataToModelMapper.pg_data_load(
                model=ReferenceInfo, data=data_objs.get("ReferenceInfo")
            )
            check = get_record_by_page_clue(
                model=ReferenceInfo, page=new_reference.page, clue=new_reference.clue
            )
            if check:
                check.info = new_reference.info
                check.link = new_reference.link
                records_to_add.append(check)
                message = f"Will update record for {check.page}: {check.clue}."
                results = {"results": check.id}
            else:
                if new_reference:
                    message = f"Creating new records for {new_reference.page}: {new_reference.clue}."
                    new_reference.id = new_id
                    records_to_add.append(new_reference)
                    results = {"results": new_reference.id}

            flash(message=message)
            logger.info(message)
            db.session.add_all(records_to_add)
            db.session.commit()
            results['status'] = 200

            return results

    def delete(self, ref_id: int) -> dict:
        """Delete a reference-info record.

        Args:
            ref_id (int): id of the record to delete
        
        Request body:
            {"clue": "clue of record to delete"}
        
        Returns:
            dict: records deleted
        """
        records_to_del = []
        data = request.get_json()
        record_check = get_record_by_id(model=self.model, id=ref_id, filters=[(ReferenceInfo.clue == data.get("clue"))])

        if record_check:
            message = f"Deleting records for id: {ref_id} clue: {data.get('clue')}"
            records_to_del.append(record_check)
            results = {"results": record_check.id}
        else:
            message = f"Record not found for id: {ref_id}"
            results = {"results": None}
        flash(message=message)
        [db.session.delete(rec) for rec in records_to_del if records_to_del]
        db.session.commit()
        results['status'] = 200

        return results

