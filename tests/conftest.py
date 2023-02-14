import json
import os

import pytest

from src import logger
from src.project.utils.load_data import load_data
from src.project.app import create_app
from src.project.models import People, PageOrder, PageRefs
from src.project.services import db

logger = logger.get_logger(__name__)

@pytest.fixture(scope="session")
def new_sqlite_db():
    pass

@pytest.fixture(scope="session")
def app():
    app_env = os.getenv("APP_ENV")
    app = create_app(app_env, testing=True)

    return app


@pytest.fixture(scope="function")
def session():
    db.session.begin_nested()
    logger.debug("Beginning nested")
    yield db.session
    logger.debug("Rolling back")
    db.session.rollback()


@pytest.fixture(scope="function")
def load_all_test_data(session, app):
    """Create a testing app context to load test data."""
    with app.app_context():
        logger.info("Loading relational data in testing app.")
        record_groups = [
            ("test_characters", People),
            ("test_page_refs", PageRefs),
            ("test_page_order", PageOrder),
        ]
        [load_data.load_pg_data(t[0], t[1]) for t in record_groups]
    return app


@pytest.fixture(scope="function")
def load_page_refs(load_people_data, session):
    """Load PageRefs and People data."""
    with open("tests/demo_data.json") as f:
        data = json.load(f)
    records = data["page_refs"]
    for record in records:
        record = PageRefs(**record)
        db.session.add(record)
    db.session.flush()
    return record


@pytest.fixture(scope="function")
def load_people_data(session):
    """Load People data."""
    # with open("tests/demo_data.json") as f:
    #     data = json.load(f)
    # records = data["people"]
    # for record in records:
    #     record = People(**record)
    #     db.session.add(record)
    # db.session.flush()
    # return record
    load_data.load_pg_data(record_group="people", model=People)


@pytest.fixture(scope="function")
def load_page_order(session):
    """Load PageOrder data."""
    load_data.load_pg_data(record_group="page_order", model=PageOrder)
