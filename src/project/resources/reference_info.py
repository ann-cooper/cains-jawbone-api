from flask import current_app, flash, redirect, render_template, request, url_for
from flask.views import MethodView
from src.project.models import ReferenceInfo
from src.project.services import db
from src.project.forms.post_ref_info_form import RefInfoForm
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.sqla_query_helper import (
    get_all_records,
    get_recent_records,
    get_record_by_id,
    get_record_by_name,
    search_records,
    get_next_id
)
from src.project.schemas import RefInfoSchema
from src import logger


logger = logger.get_logger(__name__)


class ReferenceInfoHandler(MethodView):
    def get(self):
        form = RefInfoForm()
        # TODO
        results = get_recent_records(model=ReferenceInfo)
        schema = RefInfoSchema()
        if results:
            results = [schema.dump(result) for result in results]
        else:
            results = {"message": "No records", "status": 200}

        return render_template("ref_info.html", form=form, results=results)

    def post(self):
        form = RefInfoForm()
        records_to_add = []
        if form.validate_on_submit():
            new_id = get_next_id(model=ReferenceInfo)
            form_data_objs = DataToModelMapper(models=[ReferenceInfo], form_data=form.data).extract_db_fields().form_unpack().new_objs
            new_reference = DataToModelMapper.pg_data_load(model=ReferenceInfo, data=form_data_objs.get('ReferenceInfo'))
            # TODO
            check = search_records(model=ReferenceInfo, filters=[(ReferenceInfo.page == new_reference.page), (ReferenceInfo.clue == new_reference.clue)])
            if check:
                check = check[0]
                logger.debug(f"check: {check} ... {dir(check)}")
                check.info = new_reference.info
                check.link = new_reference.link
                records_to_add.append(check)
                flash(f"Will update record for {check.page}: {check.clue}.")
            else:
                if new_reference:
                    flash(f"Creating new records for {new_reference.page}: {new_reference.clue}.")
                    new_reference.id = new_id
                    records_to_add.append(new_reference)

            db.session.add_all(records_to_add)
            db.session.commit()
            return redirect(url_for("reference_info_handler"))
