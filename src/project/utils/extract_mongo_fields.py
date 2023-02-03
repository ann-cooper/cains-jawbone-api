import attr
from src import logger

logger = logger.get_logger(__name__)


class DocDataToModelMapper:
    def __init__(self,  models, form_data, ignore_fields=['_id', 'created_date']):
        self.models = models
        self.form_data = form_data
        self.ignore_fields = ignore_fields
        self.keys_dict = None
        self.new_objs = None

    def extract_doc_fields(self):

        self.keys_dict = {
            model.__name__: [att.name for att in model.__attrs_attrs__ if att.name not in self.ignore_fields]
            for  model in self.models
            }
        return self

    def form_unpack(self):
        self.new_objs = {}
        for model in self.models:
            model_name = model.__name__
            form_data_obj = {key: self.form_data.get(key) for key in self.keys_dict.get(model_name)}
            self.new_objs[model_name] = form_data_obj
        return self

    @staticmethod
    def data_load(model, data):
        try:
            new_obj = model(**data)
        except Exception as err:
            logger.warn(f"Error: {err} in data_load")
        else:
            logger.debug(f"New object loaded: {new_obj} type: {type(new_obj)}")
            return new_obj