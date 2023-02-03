from flask import current_app, flash, redirect, render_template, request, url_for
from flask.views import MethodView

from src import logger
from src.project.forms.delete_records_form import DelRecordsForm
from src.project.forms.post_character_form import CharacterForm
from src.project.models import PageOrder, PageRefs, People
from src.project.schemas.people_schema import PeopleSchema
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper
from src.project.utils.sqla_query_helper import (
    find_model,
    get_all_records,
    get_recent_records,
    get_record_by_id,
    get_record_by_name,
    search_records,
)

logger = logger.get_logger(__name__)


class PageInfoHandler(MethodView):
    def get(self):
        pass

    def post(self):
        pass
