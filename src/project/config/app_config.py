import os


class DefaultConfig:

    APP_ENV = os.getenv("APP_ENV", "local")
    DEBUG = True
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    # Postgres
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Re: deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(DefaultConfig):
    pass


class ProdConfig(DefaultConfig):
    pass


CONFIGURATIONS = {"local": LocalConfig, "prod": ProdConfig, "dev": LocalConfig}
