import json
from typing import Union

import pytest

from src import logger
from src.project.app import create_app
from src.project.forms import CharacterForm, DelRecordsForm, RefInfoForm
from src.project.models import PageOrder, PageRefs, People, ReferenceInfo
from src.project.services import db
from src.project.utils.load_data import load_pg_data

logger = logger.get_logger(__name__)


@pytest.fixture(scope="session", autouse=True)
def app():
    app_env = "test"
    app = create_app(app_env)
    yield app


@pytest.fixture(scope="function")
def clean_test_tables(app):
    yield
    table_models = [People, PageOrder, PageRefs, ReferenceInfo]
    for table in table_models:
        try:
            table.query.delete()
            db.session.commit()
        except Exception as err:
            logger.warning(f"Error trying to clean records from {table}: {err}")
    db.create_all()
    load_all_test_data()


@pytest.fixture(scope="function")
def empty_test_tables(app):
    table_models = [People, PageOrder, PageRefs, ReferenceInfo]
    for table in table_models:
        try:
            table.query.delete()
            db.session.commit()
        except Exception as err:
            logger.warning(f"Error trying to clean records from {table}: {err}")
    db.create_all()


@pytest.fixture(scope="function")
def people_form_data():
    with open("tests/demo_data.json", "r") as f:
        data = json.load(f)
    return data.get("people_form_data")


@pytest.fixture(scope="function")
def page_refs_form_data():
    with open("tests/demo_data.json", "r") as f:
        data = json.load(f)
    return data.get("page_info_form_data")


def load_all_test_data():
    """Create a testing app context to load test data."""

    logger.info("Loading relational data in testing app.")
    record_groups = [
        ("people_records", People),
        ("page_refs_records", PageRefs),
        ("page_order_records", PageOrder),
        ("reference_info_records", ReferenceInfo),
    ]
    [load_pg_data(t[0], t[1]) for t in record_groups]
