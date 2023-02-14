from flask import flash, redirect, render_template, request, url_for
from flask.views import MethodView

from src import logger
from src.project.forms.delete_records_form import DelRecordsForm
from src.project.models import PageRefs
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    find_model,
    get_all_records,
    get_record_by_id,
)

logger = logger.get_logger(__name__)


class RecordsCleanup(MethodView):
    """Remove records"""

    def __init__(self):
        self.form = DelRecordsForm()

    def get(self, model):
        logger.debug(f"Delete: {model} ... {request.view_args}")
        model = request.view_args.get("model")
        logger.debug(f"Delete: {model}")
        model_dict = find_model(key=model)
        schema = model_dict.get("schema")()
        model = model_dict.get("model")
        results = dump_recent_records(model=model, schema=schema)
        results = results if results else {"message": "No records", "status": 200}

        return render_template("delete_records.html", form=self.form, results=results)

    def post(self, model):
        logger.debug(f"Delete post {model}")
        records_to_del = []

        if self.form.validate_on_submit():
            model_dict = find_model(key=request.form.get("record_type"))
            model = model_dict.get("model")
            # schema = model_dict.get("schema")()
            model_name = model().__class__.__name__
            logger.debug(f"Prep delete of {self.form.data}")
            form_data_objs = (
                DataToModelMapper(models=[model], form_data=self.form.data)
                .extract_db_fields()
                .form_unpack()
                .new_objs
            )
            new_obj = DataToModelMapper.pg_data_load(
                model=model, data=form_data_objs.get(model_name)
            )
            record_check = get_record_by_id(model=model, id=new_obj.id)

            if record_check:
                logger.debug(
                    f"Found {model_name} record to delete for {record_check.id}. "
                )
                message = f"Deleting records for {record_check.id}"
                records_to_del.append(record_check)
                if model_name == "People":
                    page_refs = get_all_records(
                        model=PageRefs, filters=[(PageRefs.name == record_check.name)]
                    )
                    if page_refs:
                        [records_to_del.append(rec) for rec in page_refs]
                        message = (
                            message
                            + f"Deleting records for {record_check.name} and pages {[x.page for x in page_refs]}"
                        )

            else:
                message = f"Record not found for {new_obj}"

            flash(message=message)
            [db.session.delete(rec) for rec in records_to_del if records_to_del]
            db.session.commit()
            return redirect(url_for("records", model=model_name.lower()))
