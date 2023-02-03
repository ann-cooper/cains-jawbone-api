from flask import flash, redirect, render_template, request, url_for
from flask.views import MethodView

from src import logger
from src.project.forms.delete_records_form import DelRecordsForm
from src.project.models import PageRefs, People
from src.project.schemas.people_schema import PeopleSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.sqla_query_helper import (
    find_model,
    get_all_records,
    get_recent_records,
    get_record_by_name,
)

logger = logger.get_logger(__name__)


class RecordsCleanup(MethodView):
    """Remove records"""

    def get(self):
        form = DelRecordsForm()
        schema = PeopleSchema()
        results = get_recent_records(model=People)
        if results is False:
            results = {"message": "No records", "status": 400}
        else:
            results = [schema.dump(rec) for rec in results]

        return render_template("delete_records.html", form=form, results=results)

    def post(self):
        form = DelRecordsForm()
        records_to_del = []

        if form.validate_on_submit():
            model_dict = find_model(key=request.form.get("record_type"))
            model = model_dict.get("model")
            schema = model_dict.get("schema")()
            model_name = model().__class__.__name__
            logger.debug(f"Prep delete of {form.data}")
            form_data_objs = (
                DataToModelMapper(models=[model], form_data=form.data)
                .extract_db_fields()
                .form_unpack()
                .new_objs
            )
            logger.debug(f"Form data objs: {form_data_objs}")
            new_obj = DataToModelMapper.pg_data_load(
                model=model, data=form_data_objs.get(model_name)
            )
            logger.debug(f"Del record: {new_obj}")
            # TODO
            record_check = get_record_by_name(model=model, name=new_obj.name)
            logger.debug(f"record_check: {record_check}")

            if record_check:
                logger.debug(
                    f"Found {model_name} record to delete for {record_check.id}"
                )
                records_to_del.append(record_check)
                if model_name == "People":
                    page_refs = get_all_records(
                        model=PageRefs, filters=[(PageRefs.name == record_check.name)]
                    )
                    logger.debug(f"page refs: {page_refs}")
                    if page_refs:
                        [records_to_del.append(rec) for rec in page_refs]
                        logger.debug(
                            f"Found page refs for pages: {[x.page for x in page_refs]}"
                        )
                        flash(
                            f"Deleting records for {record_check.name} and pages {[x.page for x in page_refs]}"
                        )
                flash(f"Deleting records for {record_check.id}")
            else:
                logger.debug(f"Record not found for {new_obj}")
            logger.debug(
                f"Deleting records for: {[schema.dump(rec) for rec in records_to_del if records_to_del]}"
            )
            [db.session.delete(rec) for rec in records_to_del if records_to_del]
            db.session.commit()
            return redirect(url_for("records"))
        # TODO    
        results = get_all_records(model=model)
        logger.debug("getting here")
        return render_template("delete_records.html", form=form, results=results)
