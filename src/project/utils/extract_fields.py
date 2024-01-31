from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import inspect

from src import logger
from src.project.services import db

logger = logger.get_logger(__name__)


class DataToModelMapper:
    """Extract form or request data.

    Attributes:
        models: list
        keys_dict: dict

    Methods:
        extract_db_fields()
            Get fields from a Sqlalchemy model.
        data_unpack(data: dict)
            Gets values from form for keys that exist in the model fields.
        pg_data_load(model: DefaultMeta, data: dict) -> db.Model
            Loads extracted data to a model.
    """

    def __init__(self, models: list):
        self.models = models
        self.keys_dict = None

    def extract_db_fields(self) -> list:
        """Get fields from Sqlalchemy models.

        Returns:
            dict: a dict of the model fields with model class name as key and fields as values
        """
        try:
            self.keys_dict = {
                model().__class__.__name__: inspect(model().__class__).c.keys()
                for model in self.models
            }
        except TypeError as err:
            logger.warn(f"Error in extract_db_fields: {err}")
            raise
        else:
            return self

    def data_unpack(self, data: dict) -> dict:
        """Gets values from form for keys that exist in the model fields.

        Returns:
            new_objs: dict
        """
        new_objs = {}
        for model in self.models:
            model_name = model().__class__.__name__
            data_obj = {key: data.get(key) for key in self.keys_dict.get(model_name)}
            new_objs[model_name] = data_obj

        return new_objs

    @staticmethod
    def pg_data_load(model: DefaultMeta, data: dict) -> db.Model:
        """Loads extracted data to a model.

        Args:
            model (slqalchemy.Model): A Sqlalchemy model
            data (dict): A dict of data to me loaded

        Returns:
            Model object: instance of the data loaded into the model
        """
        try:
            new_obj = model(**data)
        except TypeError as err:
            logger.warn(f"Error: {err} in pg_data_load")
            raise
        else:
            logger.info(f"New object loaded: {type(model)} type: {type(new_obj)}")
            return new_obj
