from flask_mongoengine import mongoengine


def mongo_dict_field_validator(val):
    """Called by mongoengine to validate the dict field 'properties'."""
    if not isinstance(val, dict):
        raise mongoengine.ValidationError("Properties field must be a dictionary.")

    if val.keys():
        if not set(val.keys()) == {"page", "clue", "refernce"}:
            raise mongoengine.ValidationError(
                "Properties contains invalid field names."
            )
