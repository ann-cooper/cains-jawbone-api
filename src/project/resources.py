from flask import render_template, request, redirect, url_for, flash, current_app
from flask.views import MethodView

from src import logger
from src.project.models.people_model import People, PageRefs
from src.project.models.pages_model import PageOrder
from src.project.services import db
from src.project.forms.post_character_form import CharacterForm
from src.project.forms.delete_records_form import DelRecordsForm
from src.project.utils.sqla_query_helper import (get_all_records,
                                                 get_record_by_id,
                                                 search_records,
                                                 get_record_by_name,
                                                 find_model,
                                                 get_recent_records)
from src.project.schemas.people_schema import PeopleSchema
from src.project.utils.extract_fields import DataToModelMapper


logger = logger.get_logger(__name__)


class Hello(MethodView):
    def get(self):
        return ({"message": "Hello!"}, 200)

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
                logger.debug(f'Found results:{results}')
            else:
                results = {"message": "No records", "status": 400}
        
        return render_template("character.html", form=form, results=results)

    def post(self):
        form = CharacterForm()
        records_to_add = []
        if form.validate_on_submit():
            records = get_all_records(model=People)
            new_id = max([rec.id for rec in records]) + 1
            logger.debug(f"new id: {new_id}")
            logger.debug(f"Records total: {records.total}")
            # logger.debug(f"Type of form: {type(form)}")
            form_data_objs = DataToModelMapper(models=[PageRefs, People], form_data=form.data).extract_db_fields().form_unpack().new_objs
            # logger.debug(f"form data objs: {form_data_objs}")
            new_character = DataToModelMapper.pg_data_load(model=People, data=form_data_objs.get("People"))
            new_page_ref = DataToModelMapper.pg_data_load(model=PageRefs, data=form_data_objs.get("PageRefs"))
            logger.debug(f"post new_character {new_character.name} {new_character.id} ... post new page ref {new_page_ref.name}, {new_page_ref.page}, {new_page_ref.people_id}")
            # Check for existing record
            character_check = get_record_by_name(model=People, name=new_character.name)
            if character_check:
                character_check.role = new_character.role
                logger.debug(f"Found character: {character_check.id}")
                records_to_add.append(character_check)
                new_page_ref.people_id = character_check.id
                pages_check = search_records(model=PageRefs, filters=[(PageRefs.page == new_page_ref.page), (PageRefs.people_id == character_check.id)])
                if pages_check.count() > 0:
                    logger.info(f"A record for page {new_page_ref.page} for character name {character_check.name} and people_id {character_check.id} already exists.")
                    flash(f'Updating record for {character_check.name} but not page_ref {new_page_ref.page} because a record for {character_check.name} on page {new_page_ref.page} exists.')
                else:
                    records_to_add.append(new_page_ref)
                    flash(f'Updating record for {character_check.name} and page_ref {new_page_ref.page}')
            else:
                flash(f"Creating new record")
                if new_character:
                    new_character.id = new_id
                    records_to_add.append(new_character)
                    new_page_ref.people_id = new_character.id
                    records_to_add.append(new_page_ref)

            db.session.add_all(records_to_add)
            db.session.commit()
            return redirect(url_for('characters'))

class RecordsCleanup(MethodView):
    """Remove records
    """  
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
            model_dict = find_model(key=request.form.get('record_type'))
            model = model_dict.get("model")
            schema = model_dict.get("schema")()
            model_name = model().__class__.__name__
            logger.debug(f"Prep delete of {form.data}")
            form_data_objs = DataToModelMapper(models=[model], form_data=form.data).extract_db_fields().form_unpack().new_objs
            logger.debug(f"Form data objs: {form_data_objs}")
            new_obj = DataToModelMapper.pg_data_load(model=model, data=form_data_objs.get(model_name))
            logger.debug(f"Del record: {new_obj}")
            record_check = get_record_by_name(model=model, name=new_obj.name)
            logger.debug(f"record_check: {record_check}")
            
            
            if record_check:
                logger.debug(f"Found {model_name} record to delete for {record_check.id}")
                records_to_del.append(record_check)
                if model_name == "People":
                    page_refs = get_all_records(model=PageRefs, filters=[(PageRefs.name == record_check.name)])
                    logger.debug(f"page refs: {page_refs}")
                    if page_refs:
                        [records_to_del.append(rec) for rec in page_refs]
                        logger.debug(f"Found page refs for pages: {[x.page for x in page_refs]}")
                        flash(f"Deleting records for {record_check.name} and pages {[x.page for x in page_refs]}")
                flash(f"Deleting records for {record_check.id}")
            else:
                logger.debug(f"Record not found for {new_obj}")
            logger.debug(f"Deleting records for: {[schema.dump(rec) for rec in records_to_del if records_to_del]}")
            [db.session.delete(rec) for rec in records_to_del if records_to_del]
            db.session.commit()
            return redirect(url_for('records'))
        results = get_all_records(model=People)
        logger.debug("getting here")
        return render_template("delete_records.html", form=form, results=results)

