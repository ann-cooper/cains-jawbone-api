from flask import flash, redirect, render_template, url_for
from flask.views import MethodView

from src import logger
from src.project.forms import PageRefForm
from src.project.models import PageRefs, People
from src.project.schemas import PageRefSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_next_id,
    get_record_by_name,
    get_record_by_page_name,
)

logger = logger.get_logger(__name__)


class PageInfoHandler(MethodView):
    def __init__(self):
        self.model = PageRefs
        self.schema = PageRefSchema()
        self.form = PageRefForm()

    def get(self):
        results = dump_recent_records(model=self.model, schema=self.schema)
        results = results if results else {"message": "No records", "status": 200}

        return render_template("page_refs.html", form=self.form, results=results)

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
            new_page_ref = DataToModelMapper.pg_data_load(
                model=self.model, data=form_data_objs.get("PageRefs")
            )
            check = get_record_by_page_name(
                model=self.model, page=new_page_ref.page, name=new_page_ref.name
            )
            if check:
                message = (
                    f"Not updating {check.page}, {check.name} because record exists."
                )
                logger.info(message)
            else:
                new_page_ref.id = new_id
                records_to_add.append(new_page_ref)
                character_check = get_record_by_name(
                    model=People, name=new_page_ref.name
                )
                message = f"New record created for {new_page_ref.page}"
                if not character_check:
                    # Create new character record
                    new_character_id = get_next_id(model=People)
                    new_character = People(name=new_page_ref.name, id=new_character_id)
                    records_to_add.append(new_character)
                    message = (
                        message
                        + f" and new character record created for {new_character.name}."
                    )
            flash(message=message)
            db.session.add_all(records_to_add)
            db.session.commit()
            return redirect(url_for("page_info_handler"))
