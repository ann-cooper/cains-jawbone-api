import json
import os

from flask_sqlalchemy.model import DefaultMeta

from src import logger
from src.project.app import create_app
from src.project.models import PageOrder, PageRefs, People, ReferenceInfo
from src.project.services import db

logger = logger.get_logger(__name__)


def app():
    """Create an app context to load test data outside of a test session."""
    app_env = os.getenv("APP_ENV")
    app = create_app(app_env, testing=True)
    with app.app_context():
        logger.info("Loading relational data.")
        record_groups = [
            ("people_records", People),
            ("page_refs_records", PageRefs),
            ("page_order_records", PageOrder),
            ("reference_info_records", ReferenceInfo),
        ]
        [load_pg_data(t[0], t[1]) for t in record_groups]
    return app


def load_pg_data(record_group: dict, model: DefaultMeta):
    """Load a dictionary of records into a relational model.

    Args:
        record_group (dict): Test data to load
        model (DefaultMeta): Model to load with
    """
    with open("tests/demo_data.json", "r") as f:
        data = json.load(f)
    for record in data[record_group]:
        record = model(**record)
        db.session.add(record)
    db.session.commit()


if __name__ == "__main__":
    app()
