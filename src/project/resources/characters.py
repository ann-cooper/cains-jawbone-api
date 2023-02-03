from flask import flash, redirect, render_template, url_for
from flask.views import MethodView

from src import logger
from src.project.forms.post_character_form import CharacterForm
from src.project.models import PageRefs, People
from src.project.schemas.people_schema import PeopleSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.sqla_query_helper import (
    get_all_records,
    get_recent_records,
    get_record_by_id,
    get_record_by_name,
    search_records,
    get_next_id
)

logger = logger.get_logger(__name__)


class Characters(MethodView):
    def get(self, character_id):
        form = CharacterForm()
        results = {}
        schema = PeopleSchema()
        if character_id is None:
            results = get_recent_records(model=People)
            if results:
                results = [schema.dump(result) for result in results]
            else:
                results = {"message": "No records", "status": 400}
        else:
            results = get_record_by_id(model=People, id=character_id)
            if results:

                results = [schema.dump(results)]
                logger.debug(f"Found results:{results}")
            else:
                results = {"message": "No records", "status": 400}

        return render_template("character.html", form=form, results=results)

    def post(self):
        form = CharacterForm()
        records_to_add = []
        if form.validate_on_submit():
            new_id = get_next_id(model=People)
            logger.debug(f"new id: {new_id}")
            # logger.debug(f"Type of form: {type(form)}")
            form_data_objs = (
                DataToModelMapper(models=[PageRefs, People], form_data=form.data)
                .extract_db_fields()
                .form_unpack()
                .new_objs
            )
            # logger.debug(f"form data objs: {form_data_objs}")
            new_character = DataToModelMapper.pg_data_load(
                model=People, data=form_data_objs.get("People")
            )
            new_page_ref = DataToModelMapper.pg_data_load(
                model=PageRefs, data=form_data_objs.get("PageRefs")
            )
            logger.debug(
                f"post new_character {new_character.name} {new_character.id} ... post new page ref {new_page_ref.name}, {new_page_ref.page}, {new_page_ref.people_id}"
            )
            # Check for existing record
            character_check = get_record_by_name(model=People, name=new_character.name)
            if character_check:
                character_check.role = new_character.role
                logger.debug(f"Found character: {character_check.id}")
                records_to_add.append(character_check)
                new_page_ref.people_id = character_check.id
                pages_check = search_records(
                    model=PageRefs,
                    filters=[
                        (PageRefs.page == new_page_ref.page),
                        (PageRefs.people_id == character_check.id),
                    ],
                )
                if pages_check.count() > 0:
                    logger.info(
                        f"A record for page {new_page_ref.page} for character name {character_check.name} and people_id {character_check.id} already exists."
                    )
                    flash(
                        f"Updating record for {character_check.name} but not page_ref {new_page_ref.page} because a record for {character_check.name} on page {new_page_ref.page} exists."
                    )
                else:
                    records_to_add.append(new_page_ref)
                    flash(
                        f"Updating record for {character_check.name} and page_ref {new_page_ref.page}"
                    )
            else:
                flash(f"Creating new record")
                if new_character:
                    new_character.id = new_id
                    records_to_add.append(new_character)
                    new_page_ref.people_id = new_character.id
                    records_to_add.append(new_page_ref)

            db.session.add_all(records_to_add)
            db.session.commit()
            return redirect(url_for("characters"))
