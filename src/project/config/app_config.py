import os


class DefaultConfig:
    APP_ENV = os.getenv("APP_ENV", "local")
    DEBUG = True
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    # Sqlite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:////tests/pg_puzzle.db"
    )
    # Mongo
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_SETTINGS = {"host": f"mongodb://{MONGODB_URI}"}

    # Re: deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(DefaultConfig):
    pass


class TestConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////code/pg_puzzle_testing.db"


CONFIGURATIONS = {"local": LocalConfig, "test": TestConfig, "dev": LocalConfig}
