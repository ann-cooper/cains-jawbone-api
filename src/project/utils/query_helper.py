from typing import Union

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import func

from src import logger
from src.project.models import PageOrder, PageRefs, People, ReferenceInfo
from src.project.schemas import (
    PageOrderSchema,
    PageRefSchema,
    PeopleSchema,
    RefInfoSchema,
)

logger = logger.get_logger(__name__)


def get_next_id(model: DefaultMeta) -> int:
    max_id = model.query.with_entities(func.max(model.id)).first()

    if max_id[0] is not None:
        return max_id[0] + 1
    else:
        return 1


def get_record_by_id(model: DefaultMeta, id: int, filters: list = None):
    """
    Return a sqlalchemy record by id or False.
    """
    filters = [] if not filters else filters
    filters.append(model.id == id)
    record = model.query.filter(*filters).one_or_none()
    if not record:
        return False
    return record


def get_record_by_name(model: DefaultMeta, name: str, filters: list = None):
    """
    Return a sqlalchemy record by name or False.
    """
    filters = [] if not filters else filters
    filters.append(model.name == name)
    record = model.query.filter(*filters).one_or_none()
    if not record:
        return False
    return record


def get_record_by_page_clue(
    model: DefaultMeta, page: int, clue: str, filters: list = None
):
    """Return record by page number and clue string or False.

    Args:
        model (sqla.Model): A sqlalchemy model
        page (int): Page number
        clue (str): Clue text
        filters (any, optional): additional filters. Defaults to None.
    """
    filters = [] if not filters else filters
    filters.append(model.page == page)
    filters.append(model.clue == clue)
    record = model.query.filter(*filters).one_or_none()
    if not record:
        return False
    logger.debug(f"get rec by page clue: {type(record)}")
    return record


def get_all_records(model: DefaultMeta, filters: list = None) -> Union[list, bool]:
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


def search_records(model: DefaultMeta, filters: list) -> Union[list, bool]:
    logger.debug(f"Using filters: {filters}")
    records = model.query.filter(*filters).all()

    if records is None:
        return False
    else:
        logger.debug(f"SEARCH Record: {records} {type(records)} {dir(records)}")
        return records


def get_record_by_page_name(
    model: DefaultMeta, page: int, name: str
) -> Union[list, bool]:
    result = model.query.filter(model.name == name, model.page == page).one_or_none()
    if not result:
        return False
    else:
        return result


def dump_recent_records(
    model: DefaultMeta, schema: any, limit: int = 5
) -> Union[list, bool]:
    records = model.query.order_by(model.id.desc()).limit(limit).all()
    logger.debug(
        f"Recent records: {type(records[0])} ... model {type(model)} ... schema {type(schema)}"
    )
    if records:
        return [schema.dump(rec) for rec in records]
    else:
        return False


def find_model(key: str) -> dict:
    """Return model class given key.

    Args:
        key (str): key from the request.form
    """
    model_map = {
        "people": {"model": People, "schema": PeopleSchema},
        "pagerefs": {"model": PageRefs, "schema": PageRefSchema},
        "pageorder": {"model": PageOrder, "schema": PageOrderSchema},
        "referenceinfo": {"model": ReferenceInfo, "schema": RefInfoSchema},
    }
    return model_map.get(key)
