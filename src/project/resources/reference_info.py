from flask import flash, redirect, render_template, url_for
from flask.views import MethodView

from src import logger
from src.project.forms import RefInfoForm
from src.project.models import ReferenceInfo
from src.project.schemas import RefInfoSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_next_id,
    get_record_by_page_clue,
)

logger = logger.get_logger(__name__)


class ReferenceInfoHandler(MethodView):
    def get(self):
        form = RefInfoForm()
        schema = RefInfoSchema()
        results = dump_recent_records(model=ReferenceInfo, schema=schema)
        results = results if results else {"message": "No records", "status": 200}

        return render_template("ref_info.html", form=form, results=results)

    def post(self):
        form = RefInfoForm()
        records_to_add = []
        if form.validate_on_submit():
            new_id = get_next_id(model=ReferenceInfo)
            form_data_objs = (
                DataToModelMapper(models=[ReferenceInfo], form_data=form.data)
                .extract_db_fields()
                .form_unpack()
                .new_objs
            )
            new_reference = DataToModelMapper.pg_data_load(
                model=ReferenceInfo, data=form_data_objs.get("ReferenceInfo")
            )
            check = get_record_by_page_clue(
                model=ReferenceInfo, page=new_reference.page, clue=new_reference.clue
            )
            if check:
                check.info = new_reference.info
                check.link = new_reference.link
                records_to_add.append(check)
                message = f"Will update record for {check.page}: {check.clue}."
            else:
                if new_reference:
                    message = f"Creating new records for {new_reference.page}: {new_reference.clue}."
                    new_reference.id = new_id
                    records_to_add.append(new_reference)

            flash(message=message)
            logger.info(message)
            db.session.add_all(records_to_add)
            db.session.commit()
            return redirect(url_for("reference_info_handler"))
