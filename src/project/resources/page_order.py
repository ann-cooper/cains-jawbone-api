from flask import current_app, flash, redirect, render_template, request, url_for
from flask.views import MethodView

from src import logger
from src.project.models import PageOrder
from src.project.services import db
from src.project.utils.extract_fields import DataToModelMapper

logger = logger.get_logger(__name__)


class PageOrderHandler(MethodView):
    def get(self):
        pass

    def post(self):
        pass
