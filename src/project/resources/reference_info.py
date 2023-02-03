from flask import current_app, flash, redirect, render_template, request, url_for
from flask.views import MethodView
from src.project.models import ReferenceInfo
import cattrs
from src.project.forms.post_ref_info_form import RefInfoForm
from src.project.utils.extract_mongo_fields import DocDataToModelMapper

from src import logger


logger = logger.get_logger(__name__)

import tinymongo as tm
import tinydb


class TinyMongoClient(tm.TinyMongoClient):
    @property
    def _storage(self):
        return tinydb.storages.JSONStorage
# Create the tinymongo service
mongo_client = TinyMongoClient('./mongo_db')
mgdb = mongo_client.references

class ReferenceInfoHandler(MethodView):
    def get(self):
        form = RefInfoForm()
        results = mgdb.references.find({},sort=[('created_date', 1)], limit=5)

        return render_template("ref_info.html", form=form, results=list(results))

    def post(self):
        form = RefInfoForm()
        if form.validate_on_submit():
            # logger.debug(f"ref info form data: {form.data}")
            data_obj = DocDataToModelMapper(models=[ReferenceInfo],form_data=form.data).extract_doc_fields().form_unpack()

            logger.debug(f"obj: {data_obj} ... data: {data_obj.new_objs}")
            check = DocDataToModelMapper.data_load(model=ReferenceInfo, data=data_obj.new_objs['ReferenceInfo'])
            record_exists = mgdb.references.find({'page': check.page, 'clue': check.clue})
            logger.debug(f"exists count: {record_exists.count()} ... {type(record_exists)}")
            # Insert one if new record
            if record_exists.count() == 0:
                logger.debug(f"check: {check}")
                data_obj.new_objs['ReferenceInfo']['created_date'] = check.created_date
                mgdb.references.insert_one(data_obj.new_objs['ReferenceInfo'])
            # Update one if record exists
            elif record_exists.count() > 0:
                logger.debug(f"Check: {check}")
                logger.debug(f"record: {record_exists.count()} ... {list(record_exists)}")
                update = mgdb.reference.update_one({'page': check.page, 'clue': check.clue}, {'$set': {'link': check.link, 'source': check.source, 'info': check.info}}, upsert=True)
                logger.debug(f"update: {dir(update)}")


            
        return redirect(url_for("reference_info_handler"))
