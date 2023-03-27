from flask import Flask
from flask_cors import CORS

from src import logger
from src.project.config.app_config import CONFIGURATIONS
from src.project.resources import (
    Characters,
    Hello,
    PageInfoHandler,
    PageOrderHandler,
    ReferenceInfoHandler,
)
from src.project.services import alembic, db, migrate, mllw

logger = logger.get_logger(__name__)


def register_endpoints(app: Flask) -> None:
    hello_view = Hello.as_view("hello")
    character_view = Characters.as_view("characters")
    page_info_view = PageInfoHandler.as_view("page_info_handler")
    page_order_view = PageOrderHandler.as_view("page_order_handler")
    reference_info_view = ReferenceInfoHandler.as_view("reference_info_handler")

    app.add_url_rule("/hello/", view_func=hello_view, methods=["GET"])
    app.add_url_rule("/characters/", view_func=character_view, methods=["GET", "POST"])
    app.add_url_rule(
        "/characters/<int:character_id>",
        view_func=character_view,
        methods=["GET", "DELETE"],
    )
    app.add_url_rule("/page-info/", view_func=page_info_view, methods=["GET", "POST"])
    app.add_url_rule("/page-info/<int:page_id>", view_func=page_info_view, methods=["GET", "DELETE"])
    app.add_url_rule("/page-order/", view_func=page_order_view, methods=["GET", "POST"])
    app.add_url_rule("/page-order/<int:order_id>", view_func=page_order_view, methods=["GET", "DELETE"])
    app.add_url_rule(
        "/reference-info/", view_func=reference_info_view, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/reference-info/<int:ref_id>", view_func=reference_info_view, methods=["GET", "DELETE"]
    )


def register_services(app: Flask, services: list) -> None:
    for service in services:
        service.init_app(app)
    migrate.init_app(app, db)


def get_config(app_env: str):
    config = CONFIGURATIONS[app_env]

    return config


def create_app(app_env: str) -> Flask:
    config = get_config(app_env)
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.FLASK_SECRET_KEY

    logger.info(
        f"Configuring app with: {config.__name__} and db {config.SQLALCHEMY_DATABASE_URI}"
    )
    CORS(app)

    register_endpoints(app)
    register_services(app, [db, mllw, alembic])

    return app
