from flask import flash, request
from flask.views import MethodView

from src import logger
from src.project.models import PageOrder
from src.project.schemas import PageOrderSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_next_id,
    get_record_by_page_order,
    get_record_by_id
)

logger = logger.get_logger(__name__)


class PageOrderHandler(MethodView):
    def __init__(self):
        self.model = PageOrder
        self.schema = PageOrderSchema()

    def get(self, order_id: int = None):
        if order_id:
            results = get_record_by_id(model=self.model, id=order_id)
            results = self.schema.dump(results) if results else None
        else:
            results = dump_recent_records(model=self.model, schema=self.schema)
        
        results = results if results else {"message": "No records", "status": 200}

        return results

    def post(self):
        records_to_add = []
        data = request.get_json()
        if data:
            new_id = get_next_id(model=self.model)
            data_objs = (
                DataToModelMapper(models=[self.model], data=data)
                .extract_db_fields()
                .data_unpack()
                .new_objs
            )
            new_page_order_record = DataToModelMapper.pg_data_load(
                model=self.model, data=data_objs.get("PageOrder")
            )
            check = get_record_by_page_order(
                model=self.model,
                order=new_page_order_record.order,
                page=new_page_order_record.page,
            )

            if check:
                message = (
                    f"Not updating {check.page}, {check.order} because record exists."
                )
                logger.info(message)
                results = {"results": None}
            else:
                new_page_order_record.id = new_id
                records_to_add.append(new_page_order_record)
                message = f"New record created for page {new_page_order_record.page} at order position {new_page_order_record.order}."
                results = {"results": new_page_order_record.id}
            flash(message=message)
            db.session.add_all(records_to_add)
            db.session.commit()
            results['status'] = 200
            return results

    def delete(self, order_id: int) -> dict:
        """Delete a page-order record.

        Args:
            order_id (int): Id of record to delete

        Request body:
            {"order": int}
            Required

        Returns:
            dict: Deleted record id
        """
        records_to_del = []
        data = request.get_json()
        order = data['order']
        record_check = get_record_by_id(model=self.model, id=order_id, filters=[(PageOrder.order == order)])

        if record_check:
            message = f"Deleting record for id: {order_id} order: {order}"
            records_to_del.append(record_check)
            results = {"results": record_check.id}
        else:
            message = f"Record not found for id: {order_id}"
            results = {"results": None}
        flash(message=message)
        [db.session.delete(rec) for rec in records_to_del if records_to_del]
        db.session.commit()
        results['status'] = 200

        return results

