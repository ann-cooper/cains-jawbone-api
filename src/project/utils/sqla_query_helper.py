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

    record = model.query.filter(*filters)
    if record is None:
        return False
    else:
        return record
