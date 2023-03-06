import json
import os

import pytest

from src import logger
from src.project.app import create_app
from src.project.models import PageOrder, PageRefs, People, ReferenceInfo
from src.project.services import alembic, db
from src.project.utils.load_data import load_pg_data

logger = logger.get_logger(__name__)


@pytest.fixture(scope="session")
def new_sqlite_db():
    # create the new db in the test session
    pass


@pytest.fixture(scope="session")
def app():
    app_env = os.getenv("APP_ENV")
    app = create_app(app_env, testing=True)

    with app.app_context():
        table_models = [People, PageOrder, PageRefs, ReferenceInfo]
        for table in table_models:
            try:
                table.query.delete()
                db.session.commit()
                logger.info(f"Cleaning {table} records for test session.")
            except Exception as err:
                logger.warning(f"Error trying to clean records from {table}: {err}")
        db.create_all()
        load_all_test_data()
    return app


@pytest.fixture(scope="function")
def session():
    db.session.begin_nested()
    logger.info("Beginning nested")
    yield db.session
    logger.info("Rolling back")
    db.session.rollback()


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
