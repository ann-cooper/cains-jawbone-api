from src import logger
from src.project.models import PageOrder, PageRefs, People, ReferenceInfo
from src.project.schemas import (
    PageOrderSchema,
    PageRefSchema,
    PeopleSchema,
    RefInfoSchema,
)
from sqlalchemy import func

logger = logger.get_logger(__name__)

def get_next_id(model):
    max_id = model.query.with_entities(func.max(model.id)).first()

    if max_id[0] is not None:
        return max_id[0] + 1
    else:
        return 1

def get_record_by_id(model, id, filters=None):
    """
    Return a sqlalchemy record by id or False.
    """
    filters = [] if not filters else filters
    filters.append(model.id == id)
    record = model.query.filter(*filters).one_or_none()
    if not record:
        return False
    return record


def get_record_by_name(model, name, filters=None):
    """
    Return a sqlalchemy record by name or False.
    """
    filters = [] if not filters else filters
    filters.append(model.name == name)
    record = model.query.filter(*filters).one_or_none()
    if not record:
        return False
    return record


def get_all_records(model, filters=None):
    """Return all records for a Sqlalchemy model.

    Args:
        model (db.Model): A Sqlalchemy model
        filters (list, optional): Additional query filters. Defaults to None.
    """
    filters = [] if not filters else filters
    records = model.query.filter(*filters).paginate()
    if records.total == 0:
        return False
    else:
        return records

def search_records(model, filters):
    logger.debug(f"Using filters: {filters}")
    records = model.query.filter(*filters).all()

    if records is None:
        return False
    else:
        #logger.debug(f"Record: {[x for x in records]}")
        return records


def get_recent_records(model):
    records = model.query.order_by(model.id.desc()).limit(3).all()
    records = records if records else False
    logger.debug(f"Recent records: {records}")
    return records


def find_model(key: str):
    """Return model class given key.

    Args:
        key (str): key from the request.form
    """
    model_map = {
        "people": {"model": People, "schema": PeopleSchema},
        "page_ref": {"model": PageRefs, "schema": PageRefSchema},
        "page_order": {"model": PageOrder, "schema": PageOrderSchema},
        "ref_info": {"model": ReferenceInfo, "schema": RefInfoSchema},
    }
    return model_map.get(key)
