from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src import logger
from src.project.config.app_config import CONFIGURATIONS
from src.project.resources import Characters, Hello
from src.project.services import alembic, mgdb, mllw, pgdb

logger = logger.get_logger(__name__)


def register_endpoints(app):

    hello_view = Hello.as_view("hello")
    app.add_url_rule("/hello/", view_func=hello_view, methods=["GET"])
    character_view = Characters.as_view("characters")
    app.add_url_rule(
        "/characters/",
        defaults={"character_id": None},
        view_func=character_view,
        methods=[
            "GET",
        ],
    )
    app.add_url_rule(
        "/characters/",
        view_func=character_view,
        methods=[
            "POST",
        ],
    )
    app.add_url_rule(
        "/characters/<int:character_id>",
        view_func=character_view,
        methods=["GET", "PUT", "DELETE"],
    )


def register_services(app, *services):

    for service in services:
        service.init_app(app)


def get_config(app_env, testing=False):

    config = CONFIGURATIONS[app_env]

    if testing is True:
        config.POSTGRES_DB += "_testing"

    return config


def create_app(app_env, testing=False):

    config = get_config(app_env, testing=testing)

    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.FLASK_SECRET_KEY

    logger.info(
        f"Configuring app with: {config.__name__} and db {config.SQLALCHEMY_DATABASE_URI}"
    )
    CORS(app)

    register_endpoints(app)
    register_services(app, pgdb, mllw, alembic, mgdb)

    migrate = Migrate(app, pgdb)
    return app
