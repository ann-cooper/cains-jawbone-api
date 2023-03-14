from flask import flash, redirect, render_template, url_for
from flask.views import MethodView

from src import logger
from src.project.forms import PageOrderForm
from src.project.models import PageOrder
from src.project.schemas import PageOrderSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_next_id,
    get_record_by_page_order,
)

logger = logger.get_logger(__name__)


class PageOrderHandler(MethodView):
    def __init__(self):
        self.model = PageOrder
        self.schema = PageOrderSchema()
        self.form = PageOrderForm()

    def get(self):
        results = dump_recent_records(model=self.model, schema=self.schema)
        results = results if results else {"message": "No records", "status": 200}

        return render_template("page_order.html", form=self.form, results=results)

    def post(self):
        records_to_add = []

        if self.form.validate_on_submit():
            new_id = get_next_id(model=self.model)
            form_data_objs = (
                DataToModelMapper(models=[self.model], form_data=self.form.data)
                .extract_db_fields()
                .form_unpack()
                .new_objs
            )
            new_page_order_record = DataToModelMapper.pg_data_load(
                model=self.model, data=form_data_objs.get("PageOrder")
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
            else:
                new_page_order_record.id = new_id
                records_to_add.append(new_page_order_record)
                message = f"New record created for page {new_page_order_record.page} at order position {new_page_order_record.order}."

            flash(message=message)
            db.session.add_all(records_to_add)
            db.session.commit()
            return redirect(url_for("page_order_handler"))
