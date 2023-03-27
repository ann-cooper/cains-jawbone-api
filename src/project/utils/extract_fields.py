from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import inspect

from src import logger
from src.project.services import db

logger = logger.get_logger(__name__)


class DataToModelMapper:
    """Extract form or request data.

    Attributes:
        models: list
        data: dict
        keys_dict: dict
        new_objs: dict

    Methods:
        extract_db_fields(self)
            Get fields from a Sqlalchemy model.
        data_unpack(self)
            Gets values from form for keys that exist in the model fields.
        pg_data_load(model: DefaultMeta, data: dict) -> db.Model
            Loads extracted data to a model.
    """
    def __init__(self, models: list, data: dict):
        self.models = models
        self.data = data
        self.keys_dict = None
        self.new_objs = None

    def extract_db_fields(self):
        """Get fields from a Sqlalchemy model.

        Args:
            model (db.Model): A sqlalchemy model

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

    def data_unpack(self):
        """Gets values from form for keys that exist in the model fields.

        Returns:
            DataModelMapper: self
        """
        self.new_objs = {}
        for model in self.models:
            model_name = model().__class__.__name__
            data_obj = {
                key: self.data.get(key) for key in self.keys_dict.get(model_name)
            }
            self.new_objs[model_name] = data_obj
        return self

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
