from flask.views import MethodView

from src import logger

logger = logger.get_logger(__name__)


class Hello(MethodView):
    def get(self):
        return ({"message": "Hello!"}, 200)
