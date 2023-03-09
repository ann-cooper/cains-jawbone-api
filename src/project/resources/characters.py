from flask import flash, redirect, render_template, url_for
from flask.views import MethodView

from src import logger
from src.project.forms.post_character_form import CharacterForm
from src.project.models import PageRefs, People
from src.project.schemas.people_schema import PeopleSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.query_helper import (
    dump_recent_records,
    get_next_id,
    get_record_by_id,
    get_record_by_name,
    search_records,
)

logger = logger.get_logger(__name__)


class Characters(MethodView):
    def __init__(self):
        self.model = People
        self.schema = PeopleSchema()
        self.form = CharacterForm()

    def get(self, character_id):
        results = {}
        if character_id is None:
            results = dump_recent_records(model=self.model, schema=self.schema)
            results = results if results else {"message": "No records", "status": 200}
        else:
            results = get_record_by_id(model=People, id=character_id)
            if results:
                results = [self.schema.dump(results)]
            else:
                results = {"message": "No records", "status": 200}

        return render_template("character.html", form=self.form, results=results)

    def post(self):
        records_to_add = []
        if self.form.validate_on_submit():
            new_id = get_next_id(model=People)
            form_data_objs = (
                DataToModelMapper(models=[PageRefs, People], form_data=self.form.data)
                .extract_db_fields()
                .form_unpack()
                .new_objs
            )
            new_character = DataToModelMapper.pg_data_load(
                model=People, data=form_data_objs.get("People")
            )
            new_page_ref = DataToModelMapper.pg_data_load(
                model=PageRefs, data=form_data_objs.get("PageRefs")
            )
            # Check for existing record
            character_check = get_record_by_name(model=People, name=new_character.name)

            if character_check:
                character_check.role = new_character.role
                records_to_add.append(character_check)
                new_page_ref.people_id = character_check.id

                pages_check = search_records(
                    model=PageRefs,
                    filters=[
                        (PageRefs.page == new_page_ref.page),
                        (PageRefs.people_id == character_check.id),
                    ],
                )
                if len(pages_check) > 0:
                    logger.info(
                        f"A record for page {new_page_ref.page} for character name {character_check.name} and people_id {character_check.id} already exists."
                    )
                    message = f"Updating record for {character_check.name} but not page_ref {new_page_ref.page} because a record for {character_check.name} on page {new_page_ref.page} exists."
                else:
                    records_to_add.append(new_page_ref)
                    message = f"Updating record for {character_check.name} and page_ref {new_page_ref.page}"
                flash(message=message)

            else:
                flash("Creating new record")
                if new_character:
                    new_character.id = new_id
                    records_to_add.append(new_character)
                    new_page_ref.people_id = new_character.id
                    records_to_add.append(new_page_ref)

            db.session.add_all(records_to_add)
            db.session.commit()
            return redirect(url_for("characters"))
