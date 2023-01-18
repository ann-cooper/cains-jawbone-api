from src import logger
from sqlalchemy import inspect

logger = logger.get_logger(__name__)

class DataToModelMapper:
    def __init__(self, models, form_data):
        self.models = models
        self.form_data = form_data
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
            self.keys_dict = {model().__class__.__name__: inspect(model().__class__).c.keys() for model in self.models}
        except Exception as err:
            logger.warn(f"Error in extract_db_fields: {err}")
        else:
            return self


    def form_unpack(self):
        """Gets values from form for keys that exist in the model fields.

        Returns:
            DataModelMapper: self
        """
        self.new_objs = {}
        for model in self.models:
            model_name = model().__class__.__name__
            form_data_obj = {key: self.form_data.get(key) for key in self.keys_dict.get(model_name)}
            self.new_objs[model_name] = form_data_obj
        return self
        
    @staticmethod
    def pg_data_load(model, data):
        """Loads extracted data to a model.

        Args:
            model (slqalchemy.Model): A Sqlalchemy model
            data (dict): A dict of data to me loaded

        Returns:
            _type_: _description_
        """
        try:
            new_obj = model(**data)
        except Exception as err:
            logger.warn(f"Error: {err} in pd_data_load")
        else:
            logger.debug(f"New object loaded: {new_obj} type: {type(new_obj)}")
            return new_obj